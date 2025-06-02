from apscheduler.schedulers.background import BackgroundScheduler
from models.news_analyzer_core.parser import MetalsNewsParser
import atexit


scheduler = BackgroundScheduler()

def run_news_analysis():
    parser = MetalsNewsParser()
    news_items = parser.parse_all_sources(max_age_hours=168)
    parser.save_to_json(news_items)


def start_scheduler():
    print('starting the news analyzer')
    run_news_analysis()

    scheduler.add_job(run_news_analysis, trigger='interval', hours=24)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
