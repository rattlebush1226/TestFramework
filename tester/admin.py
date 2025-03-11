from django.contrib import admin
from django.db import models
from django.forms import Textarea  # 明确导入Textarea组件
from django.db import models
from django.contrib import messages
from django.contrib import admin
from .models import TestCase, TestResult


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
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
    )

    list_display = ('name', 'url', 'method', 'is_active')
    # 必须配置的字段
    #list_display = ('name', 'url', 'method', 'is_active')
    list_editable = ('is_active',)  # 确保可编辑字段存在
    actions = ['custom_action']  # 如果有自定义动作
    # 新增自定义操作
    actions = ['run_selected_tests']

    def run_selected_tests(self, request, queryset):
        from .tasks import run_test_suite
        run_test_suite(queryset=queryset)  # 传递选中项

        self.message_user(request,
                          f"已执行 {queryset.count()} 个用例",
                          messages.SUCCESS
                          )

    run_selected_tests.short_description = "▶ 执行选中用例"

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('test_case', 'run_time', 'is_success')
    list_filter = ('is_success', 'run_time')

