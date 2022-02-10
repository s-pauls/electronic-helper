from django.shortcuts import render


def index(request):
    # from .tasks import run_jobs
    # run_jobs()
    return render(request, 'main/index.html')
