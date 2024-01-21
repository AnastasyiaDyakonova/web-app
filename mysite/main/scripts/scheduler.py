from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command

def execute_script():
    """Вызывается файл tran_dwh на исполнение. Устанавливается расписание, каждый день в 22 часа 51 минуту."""
    call_command('runscript', 'tran_dwh')
scheduler = BackgroundScheduler()
scheduler.add_job(execute_script, 'cron', hour=22, minute='51')

def start_scheduler():
    """Функция для запуска планировщика задач."""
    scheduler.start()

def stop_scheduler():
    """Функция для остановки планировщика задач."""
    scheduler.shutdown()