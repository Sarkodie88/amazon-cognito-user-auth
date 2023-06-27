"""
Defines the various responses to be passed across.
The necessay status codes should be seen here.

400 - response for values not found
401 - response for bad path
402 - response for bad method
403 - response for bad content
500 - general errors within the application
200 - successful response
201 - created response
"""
import json, datetime
from aws_lambda_powertools.event_handler import Response, content_types
from aws_lambda_powertools.shared.cookies import Cookie
from decimal import Decimal




def proxy_response(status_code, body=None):
     return Response(
        status_code=status_code,
        content_type=content_types.APPLICATION_JSON,
        body=json.dumps(body, default=myconverter) if body else "",
    )


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
    if isinstance(o, datetime.date):
        return o.__str__()
    if isinstance(o, Decimal):
        return round(o.__float__(), 2)
    if isinstance(o, datetime.time):
        return o.__str__()


# def proxyResponse(data):
#     return {"statusCode":200, "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},"body":json.dumps(data, default = myconverter)}
    
