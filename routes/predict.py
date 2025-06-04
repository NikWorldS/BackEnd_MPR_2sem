import os
import json

from dateutil.parser import isoparse
from flask import request, jsonify

from cache.model_cache import models
from models.predictor_core.predictor import Predictor
from utils.parser_registry import PARSERS
from utils.response_builder import build_response
from utils.resolution_utils import get_exchange_resolution
from utils.ticker_utils import is_valid_ticker
from utils.status_store import is_training, set_training_status
from services.tasks import train_model_task



def init(app, redis_cache):

    @app.route("/api/predict", methods=['POST'])
    def predict():
        data = request.get_json()
        date_from = data.get('from')
        date_to = data.get('to')
        internal_resolution = data.get('resolution')
        ticker = data.get('ticker')
        sec_id = data.get('sec_id')

        date_from = isoparse(date_from)
        date_to = isoparse(date_to)

        if sec_id not in PARSERS:
            return jsonify({"error": f'Unknown sec_id: {sec_id}'}), 400
        if not is_valid_ticker(ticker):
            return jsonify({"error": f"ticker '{ticker}' is not supported"}), 400

        resolution = get_exchange_resolution(sec_id, internal_resolution)
        if resolution is None:
            return jsonify({"error": f"Unknown resolution: '{internal_resolution}'"}), 400

        redis_key = f"predict:{sec_id}:{ticker}:{internal_resolution}:{date_from.isoformat()}:{date_to.isoformat()}"
        if redis_cache.exists(redis_key):
            cached_response = json.loads(redis_cache.get(redis_key))
            return jsonify(cached_response)

        model_key = f"{sec_id}_{ticker}_{internal_resolution}"
        model_path = os.path.join("models", "storage", model_key)

        parser_class = PARSERS[sec_id]
        parser = parser_class(ticker, resolution, date_from, date_to)
        df = parser.fetch_data()
        values = df["close"].values

        if model_key in models:
            predictor = models[model_key]
        elif os.path.exists(model_path):
            predictor = Predictor(model_path)
            models[model_key] = predictor
        else:
            if is_training(redis_cache, model_key):
                response = build_response('exodus', values, df.index)

                return jsonify({
                    "training": True,
                    "message": "Model is currently training",
                    "data": response
                }), 202
            else:
                set_training_status(redis_cache, model_key)
                train_model_task.delay(model_key, sec_id, ticker, resolution)

                response = build_response('exodus', values, df.index)
                return jsonify({
                    "training": True,
                    "message": "Model training started",
                    "data": response
                }), 202
        try:
            predicted = predictor.predict_with_dates(data=df, return_df=True)
        except ValueError as ex:
            return jsonify({"error": repr(ex)}), 400

        response = build_response('exodus', values, df.index)
        response.extend(build_response('predicted', predicted['close'], predicted.index))

        redis_cache.setex(redis_key, 172800, json.dumps(response)) # expire for 2 days

        return jsonify(response), 200
