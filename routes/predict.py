import os
import json

from dateutil.parser import isoparse
from flask import request, jsonify

from cache.model_cache import models
from models.core.model_trainer import ModelTrainer
from models.core.predictor import Predictor
from utils.parser_registry import PARSERS
from utils.time_utils import get_resolution
from utils.resolution_utils import is_valid_resolution


def init(app, redis_cache):

    @app.route("/api/predict", methods=['POST'])
    def predict():
        data = request.get_json()
        date_from = data.get('from')
        date_to = data.get('to')
        resolution = data.get('resolution')
        ticker = data.get('ticker')
        sec_id = data.get('sec_id')

        date_from = isoparse(date_from)
        date_to = isoparse(date_to)

        if sec_id not in PARSERS:
            return jsonify({"error": f'Unknown sec_id: {sec_id}'}), 400
        if not is_valid_resolution(sec_id, resolution):
            return jsonify({"error": f"Resolution '{resolution}' is not supported for {sec_id}."})

        redis_key = f"predict:{sec_id}:{ticker}:{resolution}:{date_from.isoformat()}:{date_to.isoformat()}"
        if redis_cache.exists(redis_key):
            cached_response = json.loads(redis_cache.get(redis_key))
            return jsonify(cached_response)

        model_key = f"{sec_id}_{ticker}_{resolution}"
        model_path = os.path.join("models", "storage", model_key)

        parser_class = PARSERS[sec_id]
        parser = parser_class(ticker, resolution, date_from, date_to)
        df = parser.fetch_data()

        if model_key in models:
            predictor = models[model_key]
        elif os.path.exists(model_path):
            predictor = Predictor(model_path)
            models[model_key] = predictor
        else:
            parser = parser_class(ticker, resolution)
            trainer = ModelTrainer(parser)
            trainer.train()
            trainer.save(model_path)
            predictor = Predictor(model_path)
            models[model_key] = predictor

        values = df["close"].values
        if values.shape[0] < predictor.window_size:
            return jsonify({"error": "Too small interval"}), 400

        predicted = predictor.predict(values[-predictor.window_size:])

        response = [
            {"type": "exodus", "value": float(v), "date": str(d)}
            for v, d in zip(values, df.index)
        ]
        response.append(
            {"type": "predicted", "value": float(predicted[0]), "date": str(df.index[-1] + get_resolution(resolution))}
        )

        redis_cache.setex(redis_key, 172800, json.dumps(response)) # expire for 2 days

        return jsonify(response), 200
