# Data Engineering Lifecycle Infrastructure on the Cloud

This repository contains the infrastructure for a Data Engineering Lifecycle on the cloud. It includes files for hosting on AWS Amplify, a Lambda function with necessary dependencies, and a test script.

## Files and Directories

- **index.zip**: Contains the `index.xml` file for AWS Amplify configuration.
- **lambda_function.zip**: Contains the Lambda function code along with its dependencies.
- **lambda_function.py**: The Python script for the Lambda function.
- **test.py**: A script to test the functionality of the Lambda function.

## Setting Up the Lambda Function

### Prerequisites

- AWS CLI configured with appropriate permissions.
- Python 3.12 installed.

### Steps to Package and Deploy the Lambda Function

1. **Create a Directory for Lambda Function Code**

    Create a directory to hold the Lambda function code and its dependencies.

    ```bash
    mkdir lambda_function_package
    cd lambda_function_package
    ```

2. **Add Your Lambda Function Code**

    Copy your `lambda_function.py` into the directory.

    ```bash
    cp /path/to/your/lambda_function.py .
    ```

3. **Install Dependencies**

    Install the `redshift_connector` and `requests` libraries into the current directory.

    ```bash
    pip install redshift_connector -t .
    pip install requests -t .
    ```

4. **Create a Deployment Package**

    Zip the contents of the directory to create a deployment package.

    ```bash
    zip -r ../lambda_function.zip .
    ```

5. **Deploy the Lambda Function**

    Use the AWS CLI to create or update your Lambda function with the deployment package.

    ```bash
    aws lambda create-function --function-name YourLambdaFunctionName \
    --zip-file fileb://../lambda_function.zip --handler lambda_function.lambda_handler \
    --runtime python3.x --role arn:aws:iam::your-account-id:role/your-lambda-execution-role
    ```

    If you are updating an existing Lambda function, use the following command:

    ```bash
    aws lambda update-function-code --function-name YourLambdaFunctionName \
    --zip-file fileb://../lambda_function.zip
    ```

## AWS Amplify Configuration

### index.xml

This repository includes an `index.xml` file for configuring AWS Amplify. The `index.xml` file is included in the `index.zip`.

To deploy the `index.xml` file to AWS Amplify, follow the standard process for setting up a new Amplify project or updating an existing one.

## Testing

### test.py

The `test.py` script is included to test the functionality of the Lambda function. Ensure you have the necessary AWS credentials and environment variables set up before running the tests.

Run the test script:

```bash
python test.py
