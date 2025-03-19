import json
import requests
from django.utils import timezone
from .models import TestCase, TestResult
import subprocess


def run_curl_preparation(curl_commands, test_case):
    results = []
    for cmd in curl_commands.split('\n'):
        cmd = cmd.strip()
        if not cmd:
            continue

        try:
            result = subprocess.run(
                cmd,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                timeout=10  # 每个命令最多执行10秒
            )
            results.append(f"[SUCCESS] {cmd}\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            results.append(f"[FAIL] {cmd}\nExit Code: {e.returncode}\nError: {e.stderr}")
            raise  # 中止后续执行

    # 将curl命令的返回值存储到TestCase模型中
    test_case.curl_preparation_result = '\n\n'.join(results)
    test_case.save()
    return '\n\n'.join(results)


def run_test_suite(queryset=None):
    # 动态获取测试范围
    test_cases = queryset if queryset else TestCase.objects.filter(is_active=True)

    for case in test_cases:
        # 执行Curl准备
        prep_result = ""
        try:
            if case.curl_preparation:
                prep_result = run_curl_preparation(case.curl_preparation, case)

            headers = json.loads(case.headers) if case.headers else {}
            data = json.loads(case.body) if case.body else None

            response = requests.request(
                method=case.method,
                url=case.url,
                headers=headers,
                data=data
            )
            actual = response.json()
            expected = json.loads(case.expected_response)

            is_success = (response.status_code == 200 and actual == expected)
            error_msg = "" if is_success else f"Status:{response.status_code}"
        except Exception as e:
            # 记录详细结果
            TestResult.objects.create(
                test_case=case,
                is_success=False,
                error_message=f"准备阶段失败: {str(e)}\n{prep_result}"
            )
            is_success = False
            error_msg = str(e)

        TestResult.objects.create(
            test_case=case,
            is_success=is_success,
            actual_response=json.dumps(actual) if is_success else error_msg,
            error_message=error_msg
        )