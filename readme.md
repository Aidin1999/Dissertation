# Data Engineering Lifecycle Infrastructure on the Cloud

This repository contains the infrastructure for a Data Engineering Lifecycle on the cloud. It includes files for hosting on AWS Amplify, a Lambda function with necessary dependencies, and a test script.

## Files and Directories

- **index.zip**: Contains the `index.xml` file for AWS Amplify configuration.
- **lambda_function.zip**: Contains the Lambda function code along with its dependencies.
- **lambda_function.py**: The Python script for the Lambda function.
- **test.py**: A script to test the functionality of the Lambda function.
- **data**: Directory containing raw data and database files.
  - **soccer.sqlite**: SQLite database file downloaded from [Kaggle Soccer Dataset](https://www.kaggle.com/datasets/hugomathien/soccer).
  - **sql_script.sql**: SQL script for building a database from the SQLite file.
  - **mwd.sql**: MySQL Workbench file with proposed SQL schema.

## Setting Up the Lambda Function

### Prerequisites

- AWS CLI configured with appropriate permissions.
- Python 3.12 or later installed.

### Steps to Package and Deploy the Lambda Function

1. **Create a Directory for Lambda Function Code**

    Create a directory to hold the Lambda function code and its dependencies:

    ```bash
    mkdir lambda_function_package
    cd lambda_function_package
    ```

2. **Add Your Lambda Function Code**

    Copy your `lambda_function.py` into the directory:

    ```bash
    cp /path/to/your/lambda_function.py .
    ```

3. **Install Dependencies Locally**

    Install the `redshift_connector` and `requests` libraries into the current directory:

    ```bash
    pip install redshift_connector -t .
    pip install requests -t .
    ```

4. **Create a Deployment Package**

    Zip the contents of the directory to create a deployment package:

    ```bash
    zip -r ../lambda_function.zip .
    ```

    **Note:** You can alternatively install dependencies directly on your local machine and create a zip package that includes both your Lambda function and the installed dependencies:

    - **Install Dependencies Locally:** 

      If you prefer, you can install the dependencies on your local machine and then manually create the zip file:

      ```bash
      pip install redshift_connector requests -t .
      zip -r lambda_function.zip lambda_function.py
      ```

    - **Upload to Lambda:** 

      Follow the deployment instructions below using the created `lambda_function.zip` file.

5. **Deploy the Lambda Function**

    Use the AWS CLI to create or update your Lambda function with the deployment package.

    To create a new Lambda function:

    ```bash
    aws lambda create-function --function-name YourLambdaFunctionName \
    --zip-file fileb://../lambda_function.zip --handler lambda_function.lambda_handler \
    --runtime python3.x --role arn:aws:iam::your-account-id:role/your-lambda-execution-role
    ```

    To update an existing Lambda function:

    ```bash
    aws lambda update-function-code --function-name YourLambdaFunctionName \
    --zip-file fileb://../lambda_function.zip
    ```

## AWS Amplify Configuration

### index.xml

This repository includes an `index.xml` file for configuring AWS Amplify. The `index.xml` file is included in the `index.zip`.

To deploy the `index.xml` file to AWS Amplify, follow these steps:

1. **Upload the Configuration File**

    - Navigate to the AWS Amplify console.
    - Either create a new Amplify project or select an existing one.
    - Upload the `index.zip` file containing the `index.xml` to the Amplify project.

2. **Configure Amplify**

    Follow the standard process for setting up or updating an Amplify project based on the uploaded configuration file.

## sql_script.sql

An SQL script for building a database schema from the SQLite file. This script is used to transform the raw data into a structured database.

## mwd.sql

MySQL Workbench file containing the proposed SQL schema. This file outlines the structure and relationships of the database tables as envisioned for the project.

## Data.zip Files

### soccer.sqlite and .csv files

This SQLite file is downloaded from [Kaggle Soccer Dataset](https://www.kaggle.com/datasets/hugomathien/soccer). It contains raw soccer data intended for non-commercial use.

## Testing

### test.py

The `test.py` script is provided to test the functionality of the Lambda function. Ensure you have the necessary AWS credentials and environment variables set up before running the tests.

Run the test script with:

```bash
python test.py
