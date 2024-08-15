from django.shortcuts import render
from django.http import HttpResponse
# imports the function from the TASKS.PY of DATAENTRY folder
from dataentry.tasks import celery_test_task


def home(request):
    return render(request, 'home.html')


# celery test
def celery_test(request):
    # execute time - consumin task here for celery execution
    celery_test_task.delay()  # calls the celery_test_task function and
    # execute this asynchronously or in the background or not at the same time
    # but we get the H3 message displayed right away.
    return HttpResponse('<h3>Function executed successfully.</h3>')
