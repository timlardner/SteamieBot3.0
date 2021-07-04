data "archive_file" "application" {
  type        = "zip"
  source_dir = "../pylib/"
  output_path = "payload-lambda.zip"
}

resource "aws_lambda_function" "run_steamie" {
  filename      = data.archive_file.application.output_path
  function_name = "run_steamie"
  role          = aws_iam_role.steamie_iam.arn
  handler       = "main.lambda_handler"
  runtime = "python3.8"
  source_code_hash = data.archive_file.application.output_sha
  layers           = [aws_lambda_layer_version.steamie_layer.arn]
  timeout = 30
  depends_on = [
    aws_iam_role_policy_attachment.lambda_logs,
    aws_cloudwatch_log_group.steamie_logs,
  ]
}

resource "null_resource" "build_python_layer" {
  provisioner "local-exec" {
    command = "./scripts/build_layer"
  }
  triggers = {
    // Uncomment to force builds of python virtual environment each time...
    // always_run = timestamp()
  }
}

data "archive_file" "layer" {
  depends_on = [null_resource.build_python_layer]
  type        = "zip"
  source_dir = ".env/"
  output_path = "payload-layer.zip"
}

resource "aws_lambda_layer_version" "steamie_layer" {
  filename            = data.archive_file.layer.output_path
  layer_name          = "steamie_layer"
  source_code_hash    = data.archive_file.layer.output_sha
  compatible_runtimes = ["python3.8"]
}

resource "null_resource" "clean_layer_env" {
  depends_on = [aws_lambda_layer_version.steamie_layer]
  provisioner "local-exec" {
    command = "rm -r .env"
  }
}
