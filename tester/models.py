from django.db import models

class TestCase(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    method = models.CharField(max_length=10, choices=[('GET', 'GET'), ('POST', 'POST')])
    headers = models.TextField(blank=True)  # JSON格式
    body = models.TextField(blank=True)     # JSON格式
    expected_response = models.TextField()  # JSON格式
    is_active = models.BooleanField(default=True)

    # 新增Curl准备字段
    curl_preparation = models.TextField(
        blank=True,
        verbose_name="CURL准备命令",
        help_text="每行一个Curl命令，按顺序执行"
    )

class TestResult(models.Model):
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    run_time = models.DateTimeField(auto_now_add=True)
    is_success = models.BooleanField()
    actual_response = models.TextField()
    error_message = models.TextField(blank=True)