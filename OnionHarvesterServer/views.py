from django.http import HttpResponse
from django.shortcuts import redirect


def index(request):
    return redirect('/dispatcher')

