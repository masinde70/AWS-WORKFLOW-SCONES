import json
import sagemaker
import boto3
import base64
import os 
from sagemaker.serializers import IdentitySerializer

s3 = boto3.resource('s3')
runtime= boto3.client('runtime.sagemaker')

# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2023-02-01-08-58-55-774" ## TODO: fill in

def lambda_handler(event, context):
    
  
 # Decode the image data
    image = base64.b64decode(event['body']['image_data'])

    # Instantiate a Predictor
    predictor = runtime.invoke_endpoint(EndpointName=ENDPOINT, ContentType='image/png', Body=image)
    
    inferences = predictor['Body'].read().decode('utf-8')
    event["inferences"] = [float(x) for x in inferences[1:-1].split(',')]
    
    # We return the data back to the Step Function    
    return {
        'statusCode': 200,
        'body': {
            "image_data": event['image_data'],
            "s3_bucket": event['s3_bucket'],
            "s3_key": event['s3_key'],
            "inferences": event['inferences'],
        }
    }
