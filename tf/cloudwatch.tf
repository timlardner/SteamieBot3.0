resource "aws_cloudwatch_event_rule" "steamie_trigger_dev" {
    name = "steamie_trigger_dev"
    description = "Fires every hour"
    schedule_expression = "rate(1 hour)"
    is_enabled = true
}

resource "aws_cloudwatch_event_target" "steamie_cron_target" {
    rule = aws_cloudwatch_event_rule.steamie_trigger_dev.name
    target_id = "run_steamie"
    arn = aws_lambda_function.run_steamie.arn
    input = "dev"
}
