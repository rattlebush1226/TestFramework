from django.contrib import admin
from django.db import models
from django.forms import Textarea, ModelForm  # 明确导入Textarea和ModelForm组件
from django.contrib import messages
from .models import TestCase, TestResult
import json


class TestCaseForm(ModelForm):
    class Meta:
        model = TestCase
        fields = '__all__'

    def clean_headers(self):
        headers = self.cleaned_data.get('headers')
        if headers:
            try:
                json.loads(headers)
            except json.JSONDecodeError:
                raise ValidationError("请求头必须是有效的JSON格式")
        return headers

    def clean_body(self):
        body = self.cleaned_data.get('body')
        if body:
            try:
                json.loads(body)
            except json.JSONDecodeError:
                raise ValidationError("请求体必须是有效的JSON格式")
        return body

    def clean_expected_response(self):
        expected_response = self.cleaned_data.get('expected_response')
        try:
            json.loads(expected_response)
        except json.JSONDecodeError:
            raise ValidationError("期望的响应结果必须是有效的JSON格式")
        return expected_response


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    form = TestCaseForm
    # 优化表单显示
    formfield_overrides = {
        models.TextField: {
            # 使用导入的Textarea类
            'widget': Textarea(attrs={
                'rows': 5,
                'style': 'font-family: monospace;',
                'placeholder': '示例:\ncurl -X GET http://api.example.com/init'
            })
        },
    }

    fieldsets = (
        ("基本配置", {
            'fields': ('name', 'url', 'method', 'is_active')
        }),
        ("CURL准备", {
            'fields': ('curl_preparation',),
            'description': '<div style="color:#888;margin-top:8px">'
                           '✅ 测试执行前按顺序运行这些CURL命令<br>'
                           '⛔ 任一命令失败将中止测试</div>'
        }),
        ("请求头", {
            'fields': ('headers',),
            'description': '<div style="color:#888;margin-top:8px">'
                           '请输入JSON格式的请求头</div>'
        }),
        ("请求体", {
            'fields': ('body',),
            'description': '<div style="color:#888;margin-top:8px">'
                           '请输入JSON格式的请求体</div>'
        }),
        ("期望结果", {
            'fields': ('expected_response',),
            'description': '<div style="color:#888;margin-top:8px">'
                           '请输入期望的JSON格式响应结果</div>'
        }),
        ("CURL返回值", {
            'fields': ('curl_preparation_result',),
            'description': '<div style="color:#888;margin-top:8px">'
                           'CURL准备命令的执行结果</div>'
        }),
        ("日期转时间戳", {
            'fields': ('date_input', 'timestamp_output'),
        }),
    )

    list_display = ('name', 'url', 'method', 'is_active', 'curl_preparation_result')
    list_editable = ('is_active',)  # 确保可编辑字段存在
    actions = ['run_selected_tests']

    def run_selected_tests(self, request, queryset):
        from .tasks import run_test_suite
        run_test_suite(queryset=queryset)  # 传递选中项

        self.message_user(request,
                          f"已执行 {queryset.count()} 个用例",
                          messages.SUCCESS
                          )

    run_selected_tests.short_description = "▶ 执行选中用例"

    class Media:
        js = ('js/date_to_timestamp.js',)

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('test_case', 'run_time', 'is_success')
    list_filter = ('is_success', 'run_time')

