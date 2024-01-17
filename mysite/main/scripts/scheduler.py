from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command

def execute_script():
    # Здесь вызывайте ваш файл на исполнение
    # Например, если ваш файл называется myscript.py:
    call_command('runscript', 'tran_dwh')

scheduler = BackgroundScheduler()
# Установите расписание, например, каждые 24 часа
scheduler.add_job(execute_script, 'cron', hour=22, minute='51')

def start_scheduler():
    scheduler.start()

def stop_scheduler():
    scheduler.shutdown()