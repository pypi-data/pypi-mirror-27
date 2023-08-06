import time
import hashlib
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from zencore.django.request import get_client_ip
from .models import Host
from .utils import get_update_code
from .utils import get_query_code


def update(request):
    hostname = request.GET.get("hostname", "").upper()
    ip = request.GET.get("ip", "")
    timestamp = request.GET.get("timestamp", "")
    code = request.GET.get("code", "")
    client_ip = get_client_ip(request)

    if (not hostname) or (not code) or (not timestamp):
        raise Http404()

    if abs(time.time() - int(timestamp)) > 60:
        raise Http404()

    host = get_object_or_404(Host, hostname=hostname)
    real_code = get_update_code(hostname, ip, timestamp, host.update_key)
    if code != real_code:
        raise Http404()

    host.ip = ip or client_ip
    host.update_time = now()
    host.save()

    return HttpResponse("OK")


def query(request):
    hostname = request.GET.get("hostname", "").upper()
    timestamp = request.GET.get("timestamp", "")
    code = request.GET.get("code", "")

    if (not hostname) or (not timestamp) or (not code):
        raise Http404()

    if abs(time.time() - int(timestamp)) > 60:
        raise Http404()

    host = get_object_or_404(Host, hostname=hostname)
    real_code = get_query_code(hostname, timestamp, host.update_key)
    if real_code != code:
        raise Http404()

    return HttpResponse(str(host.ip))
