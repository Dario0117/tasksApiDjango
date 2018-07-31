import json

def getDict(byte_str):
    # Parse bytes to string
    raw_str = byte_str.decode('utf-8')
    if raw_str == '':
        return {}
    # Parse string to dict
    return json.loads(raw_str.replace('\'', '\"'))

def hasRequiredParams(param_list, requiredParams):
    params_on_body = param_list.keys()
    for param in requiredParams:
        if not param in params_on_body:
            return False
    return True
