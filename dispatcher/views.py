import datetime
import json
import uuid
import csv

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from dispatcher.models import Pool, Response
from decouple import config


def index(request):
    timeout = config('TIMEOUT', cast=int)
    range_limit = config('RANGE_LIMIT', cast=int)
    pools = Pool.objects.order_by('-create_time')[:50]
    for p in pools:
        dt = datetime.datetime.now(datetime.timezone.utc) - p.dis_time
        p.days = dt.days
        p.hours = dt.seconds // 3600
        p.minutes = (dt.seconds // 60) % 60
        p.seconds = dt.seconds % 60
        p.failed = False
        p.color = 'black'
        p.dis_time = "%02d:%02d" % (p.minutes, p.seconds)
        if p.days > 0 or p.hours > 0 or p.minutes >= timeout:
            p.failed = True
            p.color = 'red'
            p.dis_time = "-"
    statistics = __get_statistics(timeout, range_limit)
    context = {
        'pools': pools,
        'clients': statistics['clients'],
        'address_ranges': statistics['address_ranges'],
        'valid_addresses': statistics['valid_addresses'],
        'timeout': timeout
    }
    return render(request, "pool/index.html", context)


def __get_statistics(timeout, range_limit):
    time_threshold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=timeout)
    params = {
        'clients': Pool.objects.filter(dis_time__gt=time_threshold).count(),
        'address_ranges': Pool.objects.count() * range_limit,
        'valid_addresses': Response.objects.count()
    }
    return params


def generate(request):
    client_id = uuid.uuid4().hex
    ports = config('PORTS', cast=lambda v: [s.strip() for s in v.split(',')])
    last_address = '7777777777777777'
    # number of addresses in range
    range_limit = config("RANGE_LIMIT", cast=int)
    # In minutes
    timeout = config('TIMEOUT', cast=int)
    this_dis_time = datetime.datetime.now(datetime.timezone.utc)
    last_range = Pool.objects.order_by('-create_time')
    timed_out_range_id = None
    if not last_range:
        address_range = __address_generator(last_address, range_limit)
    else:
        timed_out_range = __get_timed_out(timeout)
        if timed_out_range:
            address_range = {
                'start': timed_out_range[0].address_range_start,
                'end': timed_out_range[0].address_range_end
            }
            timed_out_range_id = timed_out_range[0].id
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
        Pool.objects.update_or_create(id=timed_out_range_id, defaults={"client_id": params['id'], "address_range_start": params['start'],
                                      "address_range_end": params['end'], "dis_time": this_dis_time})
        this_result = json.dumps(params)
    except Exception as e:
        this_result = "Some thing is wrong! Please try again later. Error: " + e.__str__()
    return HttpResponse(this_result, content_type="application/json")


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
    this_result = Pool.objects.filter(dis_time__lt=time_threshold).order_by('create_time')
    return this_result


@csrf_exempt
def response(request):
    if not request.POST.get('id', False):
        this_result = "Please give some parameters."
    else:
        this_client_id = request.POST['id']
        addresses = []
        if request.POST.get('addresses', False):
            addresses = json.loads(request.POST['addresses'])
        complete = request.POST.get('complete', False)
        try:
            old_pool = Pool.objects.get(client_id=this_client_id)
            for x in addresses:
                Response.objects.create(address=x[0], port=x[1], check_time=x[2])
            if complete == "true":
                old_pool.delete()
            this_result = "Thanks for contribution."
        except Exception as e:
            this_result = "Some thing is wrong! Please try again later. Error: " + e.__str__()
    return HttpResponse(this_result, content_type="application/json")


def result(request):
    responses = Response.objects.order_by('-save_time')[:15]
    context = {
        'responses': responses,
    }
    return render(request, "response/index.html", context)


def download(request):
    this_download = HttpResponse(content_type='text/csv')
    this_download['Content-Disposition'] = 'attachment; filename="onion-addresses.csv"'
    model = Response.objects.all()
    writer = csv.writer(this_download)
    writer.writerow(['Address', 'Port', 'CheckTime', 'SaveTime'])
    for m in model:
        writer.writerow([m.address, m.port, m.check_time, m.save_time])
    return this_download

