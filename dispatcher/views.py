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
    # 128 addresses in range
    range_limit = 128
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


def domain_generator(last_domain):
    chars_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
             'v', 'w', 'x', 'y', 'z', '2', '3', '4', '5', '6', '7']
    chars = list(last_domain)
    for i, e in reversed(list(enumerate(chars))):
        if e == '7':
            chars[i] = 'a'
        else:
            index = i
            char_index = chars_list.index(e)
            break
    next_multi_pre_start_char = char_index + 1
    chars[index] = chars_list[next_multi_pre_start_char]
    end_chars = chars
    print(''.join(chars))
    next_pre_end_char = chars_list.index(chars[14]) + 3
    end_chars[14] = chars_list[next_pre_end_char]
    end_chars[15] = '7'
    print(''.join(end_chars))


def get_timed_out(timeout):
    time_threshold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=timeout)
    result = Pool.objects.filter(dis_time__lt=time_threshold)[0]
    return result

