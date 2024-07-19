import requests
import json
import concurrent.futures

# Template for the message to be sent
message_template = '{}|select * from country limit 10'

# Replace with the full URL of your deployed API Gateway endpoint
api_gateway_endpoint = '**************'

# Define headers with content type for JSON data
headers = {'Content-Type': 'application/json'}

def send_message_to_sqs(message_body, api_gateway_endpoint, headers):
    """
    Sends a message to the API Gateway endpoint.

    Args:
        message_body (str): The message content to be sent.
        api_gateway_endpoint (str): The URL of the deployed API Gateway endpoint.
        headers (dict): Headers to include in the request.

    Returns:
        str or None: The response message from the API Gateway (if successful), otherwise None.
    """
    try:
        # Prepare the message data as JSON
        data = json.dumps({'message': message_body})

        # Send POST request to the API Gateway endpoint
        response = requests.post(api_gateway_endpoint, headers=headers, data=data)
        response.raise_for_status()  # Raise exception for non-2xx status codes

        # Return the response message for verification
        return response.text
    except requests.exceptions.RequestException as error:
        print(f'Error sending message to API Gateway: {error}')
        return None

def simulate_requests(num_requests):
    """
    Simulates sending multiple requests to the API Gateway using concurrent execution.

    Args:
        num_requests (int): Number of requests to send.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Create a list of message bodies for the requests
        message_bodies = [message_template.format(i) for i in range(1, num_requests + 1)]

        # Submit tasks to the executor
        futures = [executor.submit(send_message_to_sqs, body, api_gateway_endpoint, headers) for body in message_bodies]

        # Process results as they complete
        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            result = future.result()
            if result:
                print(f'Response for request {i}: {result}')
            else:
                print(f'Failed to send message for request {i}.')

# Simulate sending 100 requests
simulate_requests(100)
