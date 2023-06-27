import os
import boto3
import json
from botocore.exceptions import ClientError
from utils import response_formatter as responses
from utils import exception_handler


client = boto3.client('cognito-idp')
cognito_client_id = os.environ.get("cognito_client_id", "ror6o78okqn6384f38quruia5")


@exception_handler.exception_handler
def sign_up_user(request_body):
    response = client.sign_up(
        ClientId = cognito_client_id,
        Username = request_body["email"],
        Password = request_body["password"]
    )
        
    return responses.proxy_response(201, {"message": "Signup successful."})



# This will be used if the user requires a code to be sent for veification and confirmation
@exception_handler.exception_handler
def confirm_user_sign_up(username, confirmationCode):
    response = client.confirm_sign_up(
        ClientId = cognito_client_id,
        Username = username,
        ConfirmationCode = confirmationCode
    )

    return responses.proxy_response(200, {"message": "Registration complete."})



@exception_handler.exception_handler
def login_user(request_body):
    response = client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        ClientId = cognito_client_id,
        AuthParameters={
            'USERNAME': request_body["email"],
            'PASSWORD': request_body["password"]},
        )
        
    sessionDetails = {
                    "TokenType": response['AuthenticationResult']['TokenType'],
                    "AccessToken": response['AuthenticationResult']['AccessToken'],
                    "IdToken": response['AuthenticationResult']['IdToken'],
                    "RefreshToken": response['AuthenticationResult']['RefreshToken']
                }
    # print(sessionDetails)
   
    return responses.proxy_response(200, sessionDetails)
  

@exception_handler.exception_handler
def sign_out_user(AccessToken):
    try:
        response = client.global_sign_out(
            AccessToken = AccessToken
        )
        return responses.proxy_response(200, {"message": "User signed out successfully."})
    except ClientError as err:
        error = json.dumps(err, default= str)
        print(error)
        return responses.proxy_response(200, {"message": "Sign out attempt unsuccessful. User may be already signed out."})


@exception_handler.exception_handler
def forgot_user_password(request_body):
    response = client.forgot_password(
        ClientId = cognito_client_id,
        Username = request_body["email"]
    )

    print(response)
    return responses.proxy_response(200, {"message": "Confirmation code sent for password reset."})
   


def confirm_forgot_password(request_body):
    try:
        response = client.confirm_forgot_password(
            ClientId = cognito_client_id,
            Username = request_body["email"],
            ConfirmationCode = request_body["confirmation_code"],
            Password = request_body["password"]
        )
        # print(response)
            
        return responses.proxy_response(200, {"message": "Password reset successful."})
    except ClientError as err:
        return responses.proxy_response(200, {"message": str(err)})
        
    
    
        
# @exception_handler.exception_handler
# def confirm_forgot_password(request_body):
#     response = client.confirm_forgot_password(
#             ClientId = cognito_client_id,
#             Username = request_body["email"],
#             ConfirmationCode = request_body["confirmation_code"],
#             Password = request_body["password"]
#         )   
#     return responses.success(msg="Password reset successful")
    
        
        
