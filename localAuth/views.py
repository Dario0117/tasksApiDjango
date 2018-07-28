from django.http import HttpResponse
from django.core.validators import validate_email
import json
from django.views.decorators.csrf import csrf_exempt

def getDict(byte_str):
    # Parse bytes to string
    raw_str = byte_str.decode('utf-8')
    # Parse string to dict
    return json.loads(raw_str.replace('\'', '\"'))

def hasRequiredParams(param_list, requiredParams):
    params_on_body = param_list.keys()
    for param in requiredParams:
        if not param in params_on_body:
            return False
    return True

def _validate(request, requiredParams):
    """
        this method return 200 if:
        - method is POST and
        - contentType is application/json and
        - has all required params and
        - email is well formated
    """
    if request.method == 'POST':
        try:
            body = getDict(request.body)
        except :
            return 400
        if request.content_type == 'application/json' and hasRequiredParams(body, requiredParams):
            try:
                validate_email(body['email'])
            except:
                return 400
            return 200
        else:
            return 400
    else:
        return 404

@csrf_exempt 
def register(request):
    requiredParams = [
        'email',
        'name',
        'password',
    ]
    code = _validate(request, requiredParams)
    if code != 200:
        return HttpResponse(status=code)
    else:
        return HttpResponse(status=code)

def login(request):
    requiredParams = [
        'email',
        'password',
    ]
    code = _validate(request, requiredParams)
    if code != 200:
        return HttpResponse(status=code)
    else:
        return HttpResponse(status=code)