from apscheduler.schedulers.blocking import BlockingScheduler
import main

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=20)
def scheduled_job():
    main.run()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('Standing by..')

sched.start()