resource "aws_iam_role" "steamie_iam" {
  name = "steamie_iam"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.steamie_iam.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

data "aws_iam_policy" "DynamoWrite" {
  arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_role_policy_attachment" "allow_steamie_dynamo" {
  role       = aws_iam_role.steamie_iam.name
  policy_arn = data.aws_iam_policy.DynamoWrite.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_dev_to_call_run_steamie" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.run_steamie.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.steamie_trigger_dev.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_prod_to_call_run_steamie" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.run_steamie.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.steamie_trigger_prod.arn
}
