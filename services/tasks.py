from celery.schedules import crontab
from celery import Celery
import redis
import os

from utils.redis_config import get_redis_url
from models.predictor_core.model_trainer import ModelTrainer
from models.predictor_core.predictor import Predictor
from cache.model_cache import models
from utils.status_store import clear_status
from utils.parser_registry import PARSERS

celery_app = Celery(
    "services.tasks",
    broker=get_redis_url(),
    backend=get_redis_url()
)

celery_app.conf.update(
    timezone="UTC",
    task_track_started=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)

celery_app.conf.beat_schedule = {
    "analyze-news-every-morning": {
        "task": "services.tasks.analyze_news_task",
        "schedule": crontab(hour=8, minute=0),  # запуск ежедневно в 8:00
    },
}

@celery_app.task(name="services.tasks.train_model_task")
def train_model_task(model_key, sec_id, ticker, resolution):
    """task for training model on background"""

    parser_class = PARSERS[sec_id]
    parser = parser_class(ticker, resolution)
    trainer = ModelTrainer(parser)
    trainer.train()
    model_path = os.path.join("models", "storage", model_key)
    trainer.save(model_path)
    models[model_key] = Predictor(model_path)

    clear_status(redis.Redis.from_url(get_redis_url()), model_key)

@celery_app.task(name="services.tasks.analyze_news_task")
def analyze_news_task():
    """Parse and save latest metal-related news"""
    from models.news_analyzer_core.parser import MetalsNewsParser

    parser = MetalsNewsParser()
    news_items = parser.parse_all_sources(max_age_hours=168)
    parser.save_to_json(news_items)
