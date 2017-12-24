import datetime

import json

from django.shortcuts import render
from django.http import HttpResponse
import uuid

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
    client_id = uuid.uuid4().hex
    ports = ['80', '443']
    last_address = '7777777777777777'
    # 128 addresses in range
    range_limit = 128
    # In minutes
    timeout = 30
    this_dis_time = datetime.datetime.now(datetime.timezone.utc)
    last_range = Pool.objects.order_by('-id')
    if not last_range:
        address_range = __address_generator(last_address, range_limit)
    else:
        timed_out_range = __get_timed_out(timeout)
        if timed_out_range:
            address_range = {
                'start': timed_out_range[0].address_range_start,
                'end': timed_out_range[0].address_range_end
            }
            client_id = timed_out_range[0].client_id
        else:
            last_address = last_range[0].address_range_end
            address_range = __address_generator(last_address, range_limit)
    params = {
        'id': client_id,
        'start': ''.join(address_range['start']),
        'end': ''.join(address_range['end']),
        'ports': ports,
        'timeout': timeout * 1000
    }
    try:
        Pool.objects.update_or_create(client_id=params['id'], defaults={"address_range_start": params['start'],
                                      "address_range_end": params['end'], "dis_time": this_dis_time})
        result = json.dumps(params)
    except Exception as e:
        result = "Some thing is wrong! Please try again later. Error:" + e.__str__()
    return HttpResponse(result, content_type="application/json")


def __address_generator(last_address, range_limit):
    start_address = __next_address_generator(last_address)
    end_address = last_address
    for i in range(range_limit):
        end_address = __next_address_generator(end_address)
    address_range = {
        'start': start_address,
        'end': end_address,
    }
    return address_range


def __next_address_generator(last_address):
    last_address = list(last_address)
    chars_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z', '2', '3', '4', '5', '6', '7']
    for i, x in reversed(list(enumerate(last_address))):
        if x == '7':
            last_address[i] = 'a'
        else:
            last_address[i] = chars_list[chars_list.index(x) + 1]
            break
    return last_address


def __get_timed_out(timeout):
    time_threshold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=timeout)
    result = Pool.objects.filter(dis_time__lt=time_threshold)
    return result


def response(request):
    this_client_id = request.POST['id']
    addresses = json.JSONDecoder(request.POST['addresses'])
    old_pool = Pool.objects.get(client_id=this_client_id)
    if old_pool:
        for x in addresses:
            try:
                Response.objects.create(x['address'], x['port'], x['time'])
                result = "Thanks for contribution."
            except Exception as e:
                result = "Some thing is wrong! Please try again later. Error:" + e.__str__()
        old_pool.delete()
    else:
        result = "Some thing is wrong! Please try again later."
    return HttpResponse(result, content_type="application/json")
