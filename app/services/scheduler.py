from apscheduler.schedulers.background import BackgroundScheduler
from app.services.neo4j_utils import update_graph_with_csv
import logging

def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(update_graph_with_csv, 'interval', hours=12)

    scheduler.start()
    logging.info("Scheduler started, graph update job added.")