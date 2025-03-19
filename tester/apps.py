from django.apps import AppConfig
from django.core.exceptions import AppRegistryNotReady
import subprocess

class TesterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tester'

    def ready(self):
        try:
            # 延迟导入相关模块
            from apscheduler.schedulers.background import BackgroundScheduler
            from django.conf import settings
            from django_apscheduler.jobstores import DjangoJobStore

            if not settings.DEBUG and not settings.TESTING:
                self.start_scheduler()
        except AppRegistryNotReady:
            # 防止在应用加载完成前执行
            pass

    def start_scheduler(self):
        scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            'tester.tasks.run_test_suite',
            trigger='cron',
            hour=2,
            minute=0,
            id="daily_test_job"
        )
        scheduler.start()