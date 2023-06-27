"""
    Main utility for parameter store operations
"""
import boto3

client = boto3.client("ssm")


def getParams(param):
    """
    Main function to fetch parameter store values
    """
    response = client.get_parameter(Name=param, WithDecryption=True)
    return response["Parameter"]["Value"]
