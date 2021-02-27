from apscheduler.schedulers.blocking import BlockingScheduler
import main

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='sat-sun', hour=20)
def scheduled_job():
    print("Running the bot")
    main.run()


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=23)
def scheduled_job():
    print("Running the bot")
    main.run()


sched.start()
