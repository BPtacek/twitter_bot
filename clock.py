from apscheduler.schedulers.blocking import BlockingScheduler
import main
import datetime

yesterday = str(datetime.date.today()-datetime.timedelta(1))
sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='sat-sun', hour=20)
def scheduled_job():
    print("Running the bot")
    main.run()


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=23)
def scheduled_job():
    print("Running the bot")
    main.run()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=7)
def scheduled_job():
    print("Running the check")
    main.check_unfinished(yesterday)


sched.start()
