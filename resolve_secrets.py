import json
import os
import shlex

import boto3


def main() -> None:
    secret_arn = os.environ.get("DB_SECRET_ARN")
    if not secret_arn:
        return

    client = boto3.client("secretsmanager", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    secret = json.loads(client.get_secret_value(SecretId=secret_arn)["SecretString"])

    print(f"export DB_USER={shlex.quote(secret['username'])}")
    print(f"export DB_PASSWORD={shlex.quote(secret['password'])}")


if __name__ == "__main__":
    main()
