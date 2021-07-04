resource "aws_dynamodb_table" "link-table" {
  name = "steamiebot"
  hash_key = "key"
  billing_mode = "PAY_PER_REQUEST"

  attribute {
    name = "key"
    type = "S"
  }
}
