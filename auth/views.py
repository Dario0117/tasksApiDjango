from django.http import HttpResponse

def _validate(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            return 200
        else:
            return 400
    else:
        return 404

def register(request):
    code = _validate(request)
    if code != 200:
        return HttpResponse(status=code)
    else:
        return HttpResponse(status=code)

def login(request):
    code = _validate(request)
    if code != 200:
        return HttpResponse(status=code)
    else:
        return HttpResponse(status=code)