import os
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from controllers import auth_controller


app = APIGatewayRestResolver()

COGNITO_CLIENT_ID = os.environ.get("cognito_client_id", "")


@app.post("/register-user")
def sign_up_user():
    request_body: dict = app.current_event.json_body
    return auth_controller.sign_up_user(request_body)


@app.post("/login-user")
def log_in_user():
    request_body: dict = app.current_event.json_body
    return auth_controller.login_user(request_body)


@app.post("/forgot-password")
def forgot_password():
    request_body: dict = app.current_event.json_body
    return auth_controller.forgot_user_password(request_body)


@app.post("/reset-password")
def confirm_forgot_password():
    request_body: dict = app.current_event.json_body
    return auth_controller.confirm_forgot_password(request_body)



def lambda_handler(event, context=None):
    return app.resolve(event, context)



