from apscheduler.schedulers.blocking import BlockingScheduler
import main

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=17)
def scheduled_job():
    print("Running the bot")
    main.run()


@sched.scheduled_job('interval', minutes=15)
def timed_job():
    print('Standing by..')


sched.start()
