import datetime

import json

import itertools
from django.shortcuts import render
from django.http import HttpResponse
from dispatcher.models import Pool, Response


def index(request):
    timeout = 30
    pools = Pool.objects.order_by('-id')[:50]
    for p in pools:
        dt = datetime.datetime.now(datetime.timezone.utc) - p.dis_time
        p.days = dt.days
        p.hours = dt.seconds // 3600
        p.minutes = (dt.seconds // 60) % 60
        p.seconds = dt.seconds % 60
        p.failed = False
        p.color = 'black'
        p.dis_time = "%02d:%02d" % (p.minutes, p.seconds)
        if p.days > 0 or p.hours > 0 or p.minutes > timeout:
            p.failed = True
            p.color = 'red'
            p.dis_time = "%s days, %02d:%02d:%02d" % (p.days, p.hours, p.minutes, p.seconds)

    context = {
        'pools': pools,
    }
    return render(request, 'pool/index.html', context)


def generate(request):
    ports = ['80', '443']
    last_address = 'aaaaaaaaaaaaaaaa'
    # It will be 150 domains for ports 80 and 443.
    # It will take about 15 minutes to complete so we give clients 30 minutes
    range_limit = 150
    # In minutes
    timeout = 30
    last_range = Pool.objects.order_by('-id')[0]
    if not last_range:
        address_range = domain_generator(last_address, range_limit)
    else:
        timed_out_range = get_timed_out(timeout)
        if timed_out_range:
            last_address = timed_out_range.address_range_end
        else:
            last_address = last_range.address_range_end
        address_range = domain_generator(last_address, range_limit)
    params = {
        'start': address_range['start'],
        'end': address_range['end'],
        'ports': ports,
        'timeout': timeout * 1000
    }
    return HttpResponse(json.dumps(params), content_type="application/json")


def domain_generator(last_domain, range_limit):
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
             'v', 'w', 'x', 'y', 'z', '2', '3', '4', '5', '6', '7']
    #for x in generate_domains(chars):
    print(generate_domains(chars))
    params = {
        'start': '',
        'end': ''
    }
    return params


def get_timed_out(timeout):
    time_threshold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=timeout)
    result = Pool.objects.filter(dis_time__lt=time_threshold)[0]
    return result


def generate_domains(chars):
    chars = ''.join([str(x) for x in chars])
    return chars
    #for x in itertools.product(chars, repeat=16):
     #   yield 'http://' + ''.join([str(y) for y in x]) + '.onion'