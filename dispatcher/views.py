from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader


def index(request):
    return HttpResponse("Hello, world. You're here.")


def generate(request):
    test = int('aa', 32)
    print(test)
    return HttpResponse("Hello, world. You're here.")
    context = {
        'test': "test2",
    }
    return render(request, 'pool/index.html', context)


def tobaseN(n,N,D="0123456789abcdefghijklmnopqrstuvwxyz"):
    return (tobaseN(n//N,N)+D[n%N]).lstrip("0") if n>0 else "0"