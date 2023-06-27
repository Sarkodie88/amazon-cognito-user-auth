import boto3
import json
from botocore.exceptions import ClientError
from utils import response_formatter as responses

client = boto3.client('cognito-idp')

def exception_handler(func):
    def innerFunction(*arg, **kwargs):
        try:
            results = func(*arg, **kwargs)
            return results 
        except client.exceptions.NotAuthorizedException as err:
            print(err)
            return responses.proxy_response(400, {"message": "Invalid credentials."})
        except client.exceptions.InvalidParameterException as err:
            print(err)
            return responses.proxy_response(400, {"message": "Invalid parameter exception"})
        except client.exceptions.UserNotFoundException as err:
            print(err)
            return responses.proxy_response(400, {"message": "User not found"})
        except client.exceptions.UsernameExistsException:
            return responses.proxy_response(400, {"message": "An account with the given email already exist."})
        except client.exceptions.NotAuthorizedException:
            return responses.proxy_response(400, {"message": "Not authorized to perform this operation."})
        except client.exceptions.ExpiredCodeException:
            return responses.proxy_response(400, {"message": "Confirmation code expired."})
        except ClientError as err:
            print(err)
            return responses.proxy_response(400, {"message": str(err)})

    return innerFunction