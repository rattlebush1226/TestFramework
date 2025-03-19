from django.shortcuts import render
from .models import TestResult
import subprocess

def test_report(request):
    results = TestResult.objects.all().order_by('-run_time')
    total = results.count()
    success = results.filter(is_success=True).count()
    return render(request, 'report.html', {
        'total': total,
        'success': success,
        'failure': total - success,
        'results': results
    })