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

data "aws_iam_policy" "DynamoWrite" {
  arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_role_policy_attachment" "allow_steamie_dynamo" {
  role       = aws_iam_role.steamie_iam.name
  policy_arn = data.aws_iam_policy.DynamoWrite.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_run_steamie" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.run_steamie.function_name
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.steamie_trigger.arn
}
