'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
scheduler.py

Handles functions that run on a hourly or daily schedule
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
from src.config import *
from src.models import *

def save_politician_ratings():
    Politician.updateGraph()
    pass

# Check models, this will save the politicians score twice a day at 12pm and 5pm. Then it will store in database
def politician_schedule():
    print("Schedule jobs to save politician stuff")
    scheduler = BackgroundScheduler({'apscheduler.timezone': 'UTC'})
    # 12pm
    scheduler.add_job(func=save_politician_ratings,
                    trigger="cron", hour=19, minute=0, second=0)
    # 5p,
    scheduler.add_job(func=save_politician_ratings,
                    trigger="cron", hour=0, minute=0, second=0)

    # scheduler.add_job(func=delete_excess_files,
    #                   trigger="cron", hour=0, minute=0, second=0)
    # # pm
    # scheduler.add_job(func=delete_excess_files,
    #                   trigger="cron", hour=19, minute=0, second=0)

    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())