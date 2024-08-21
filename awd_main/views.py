from django.http import HttpResponse
from django.shortcuts import render

from dataentry.task import celery_test_task


def home(request):
    return render(request, "home.html")


def celery_test(request):
    celery_test_task.delay()
    return HttpResponse("<h1>Task completed successfully!</h1>")
