# Simple AWS Lambda Terraform Example
# requires 'lambda_handler.py' in the same directory
# to test: run `terraform plan`
# to deploy: run `terraform apply`

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "lambda_handler.py"
  output_path = "lambda_function.zip"
}

resource "aws_lambda_function" "test_lambda" {
  filename         = "lambda_function.zip"
  function_name    = "lambda_handler"
  role             = aws_iam_role.iam_for_lambda_tf.arn
  handler          = "lambda_handler.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.8"
  layers           = ["arn:aws:lambda:${var.aws_region}:634166935893:layer:vault-lambda-extension:12"]

  environment {
    variables = {
      VAULT_ADDR          = var.VAULT_ADDR,
      VAULT_AUTH_PROVIDER = "aws",
      VAULT_AUTH_ROLE     = "vault-lambda-role",
      VAULT_SECRET_PATH   = "pipeline/lambda/data",
      VAULT_SECRET_FILE   = "/tmp/vault_secret.json",
      VAULT_SKIP_VERIFY   = "true"
    }
  }
}

resource "aws_iam_role" "iam_for_lambda_tf" {
  name               = "iam_for_lambda_tf"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}


data "aws_lambda_invocation" "lambda_handler" {
  function_name = aws_lambda_function.test_lambda.function_name
  input         = <<JSON
{
  "body": {
    "message": "I am your father"
  }
}
JSON
}

output "result_entry" {
  value = jsondecode(data.aws_lambda_invocation.lambda_handler.result)
}
