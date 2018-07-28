from django.http import HttpResponse
from django.core.validators import validate_email
import json
from django.views.decorators.csrf import csrf_exempt

def _validate_email(body):
    try:
        # Parse bytes to string
        bodyString = body.decode('utf-8')
        # Parse string to dict
        params = json.loads(bodyString.replace('\'', '\"'))
        if params:
            try:
                validate_email(params['email'])
            except:
                return 400
        else:
            return 400
    except:
        return 400
    return 200

def _validate(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            return _validate_email(request.body)
        else:
            return 400
    else:
        return 404

@csrf_exempt 
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