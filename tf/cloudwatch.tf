resource "aws_cloudwatch_event_rule" "steamie_trigger_dev" {
  name                = "steamie_trigger_dev"
  description         = "Fires every hour"
  schedule_expression = "cron(0 * * * ? *)"
  is_enabled          = false
}

resource "aws_cloudwatch_event_target" "steamie_cron_target_dev" {
  rule      = aws_cloudwatch_event_rule.steamie_trigger_dev.name
  target_id = "run_steamie"
  arn       = aws_lambda_function.run_steamie.arn
  input     = "{\"env\":\"dev\", \"start_time\": 6, \"end_time\": 22}"
}

resource "aws_cloudwatch_event_rule" "steamie_trigger_prod" {
  name                = "steamie_trigger_prod"
  description         = "Fires every hour"
  schedule_expression = "cron(0 * * * ? *)"
  is_enabled          = true
}

resource "aws_cloudwatch_event_target" "steamie_cron_target_prod" {
  rule      = aws_cloudwatch_event_rule.steamie_trigger_prod.name
  target_id = "run_steamie"
  arn       = aws_lambda_function.run_steamie.arn
  input     = "{\"env\":\"prod\", \"start_time\": 6, \"end_time\": 20}"
}

resource "aws_cloudwatch_log_group" "steamie_logs" {
  name              = "/aws/lambda/run_steamie"
  retention_in_days = 7
}
