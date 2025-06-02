from celery import Celery
import redis
import os

from models.predictor_core.model_trainer import ModelTrainer
from models.predictor_core.predictor import Predictor
from cache.model_cache import models
from utils.redis_config import get_redis_url
from utils.status_store import clear_status



celery_app = Celery(
    'tasks',
    broker=get_redis_url()
)

celery_app.conf.update(
    timezone='UTC',
    task_track_started=True,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
)

@celery_app.task
def train_model_task(model_key, sec_id, ticker, resolution):
    """task for training model on background"""
    from utils.parser_registry import PARSERS

    parser_class = PARSERS[sec_id]
    parser = parser_class(ticker, resolution)
    trainer = ModelTrainer(parser)
    trainer.train()
    model_path = os.path.join("models", "storage", model_key)
    trainer.save(model_path)
    models[model_key] = Predictor(model_path)

    clear_status(redis.Redis.from_url(get_redis_url()), model_key)