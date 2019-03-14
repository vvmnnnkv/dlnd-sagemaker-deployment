# We need to use the low-level library to interact with SageMaker since the SageMaker API
# is not available natively through Lambda.
import boto3

ENDPOINT_NAME = ""

def lambda_handler(event, context):
    
    if 'body' not in event or event['body'] is None or len(event['body']) == 0:
        statusCode = 400
        result = "Missing or empty 'body' parameter"
    else:
        try:
            # The SageMaker runtime is what allows us to invoke the endpoint that we've created.
            runtime = boto3.Session().client('sagemaker-runtime')
        
            # Now we use the SageMaker runtime to invoke our endpoint, sending the review we were given
            response = runtime.invoke_endpoint(EndpointName = ENDPOINT_NAME,    # The name of the endpoint we created
                                               ContentType = 'text/plain',                 # The data format that is expected
                                               Body = event['body'])                       # The actual review
        
            # The response is an HTTP response whose body contains the result of our inference
            statusCode = 200
            result = response['Body'].read().decode('utf-8')
        except:
            statusCode = 500
            result = "Failed to get response from the model"

    return {
        'statusCode' : statusCode,
        'headers' : { 'Content-Type' : 'text/plain', 'Access-Control-Allow-Origin' : '*' },
        'body' : result
    }
