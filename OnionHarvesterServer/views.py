from django.http import HttpResponse


def index(request):
    return HttpResponse("Onion Harvester Server")
