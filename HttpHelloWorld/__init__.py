import logging
import hashlib

import azure.functions as func
FUNCTION_NAME = 'HttpHelloWorld'

def main(req: func.HttpRequest) -> func.HttpResponse:
    source_ip = ''
    if "x-forwarded-for" in req.headers:
        source_ip = req.headers["x-forwarded-for"].split(':')[0]
        
    logging.info(f'{FUNCTION_NAME}:Python HTTP trigger function processed a request from IP:[{source_ip}]')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
    
    headers = ("{}:\t{}".format(k, v) for k, v in req.headers.items())
    headers_string = "\n".join(headers)
    if name:
        md5 = hashlib.md5(name.encode('utf-8')).hexdigest()
        return func.HttpResponse(
            f"SUCCESS\nname:{name}\nmd5:{md5}\nip:{source_ip}\n\nHEADERS:\n{headers_string}",
            status_code=200
        )
    else:
        return func.HttpResponse(
             f"SUCCESS\nname: None\nip:{source_ip}\n\nHEADERS BEGIN:\n{headers_string}\n\nHEADERS END",
             status_code=200
        )
