import os
import json
import redshift_connector
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal

# Retrieve environment variables
redshift_endpoint = os.environ['REDSHIFT_SERVERLESS_ENDPOINT']
redshift_db = os.environ['REDSHIFT_SERVERLESS_DATABASE']
redshift_user = os.environ['REDSHIFT_SERVERLESS_USER']
redshift_password = os.environ['REDSHIFT_SERVERLESS_PASSWORD']
dynamodb_table_name = os.environ['DYNAMODB_TABLE_NAME']

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table_name)

def connect_to_redshift():
    """
    Establishes a connection to the Redshift workspace.
    """
    try:
        conn = redshift_connector.connect(
            host=redshift_endpoint,
            database=redshift_db,
            user=redshift_user,
            password=redshift_password,
            port=5439  # Default Redshift port
        )
        return conn
    except Exception as error:
        print(f'Error connecting to Redshift: {error}')
        return None

def execute_query(conn, query):
    """
    Executes a SQL query on the connected Redshift cluster.
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        return [dict(zip(columns, row)) for row in rows]
    except Exception as error:
        print(f'Error executing query: {error}')
        return str(error)

def save_to_dynamodb(id, result):
    """
    Saves the result to DynamoDB.
    """
    try:
        table.put_item(
            Item={
                'ID': id,
                'Result': result
            }
        )
    except ClientError as e:
        print(f'Error saving to DynamoDB: {e.response["Error"]["Message"]}')

def json_serial(obj):
    """
    JSON serializer for objects not serializable by default json code.
    """
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

def lambda_handler(event, context):
    """
    Lambda handler function that receives an SQS message, queries Redshift,
    and saves the result to DynamoDB.
    """
    try:
        message_body = json.loads(event['Records'][0]['body'])
        id, query = message_body['message'].split('|', 1)
    except (KeyError, json.JSONDecodeError, ValueError) as error:
        print(f'Error parsing SQS message: {error}')
        return

    conn = connect_to_redshift()
    if conn is None:
        save_to_dynamodb(id, 'Error connecting to Redshift')
        return

    query_result = execute_query(conn, query)
    conn.close()

    if query_result is not None:
        try:
            result = json.dumps(query_result, default=json_serial)
        except TypeError as e:
            result = f'Error serializing query result: {e}'
            print(result)
    else:
        result = 'Error executing query'
        print(result)

    # Save the result or error to DynamoDB
    save_to_dynamodb(id, result)
