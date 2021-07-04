# SteamieBot 3.0

### Usage

`cd` to the `tf` directory and run the following:
1. `terraform init`
2. `terraform apply`

You'll need to manually add your credentials to DynamoDB, either manually via the [UI](https://console.aws.amazon.com/dynamodb/home)
or using the `populate_dynamodb_*` helper scripts that you'll find in `pylib/utils.py`. These are designed to be run locally
prior to running SteamieBot on AWS.

### Requirements

* An AWS account
* Docker
* Terraform

### Testing

Most of the tests here are integration tests - mocking the [PRAW](https://praw.readthedocs.io/en/latest/) API is a pain,
so we use a Reddit account dedicated to testing. We actually hit the Reddit, YouTube and DarkSky API endpoints to test
our integrations. The only thing we don't touch during testing is AWS - instead we mock the DynamoDB endpoint using
[Moto](http://docs.getmoto.org/en/latest/), since that's where we store our secrets.

In production, all authentication information is stored in DynamoDB. In testing, these are set in environment variables.

### Environments

SteamieBot has rudimentary support for environments - each trigger contains an environment name, so a user can either
trigger a development flow that posts to a test subreddit. We do not currently support running different versions of the
lambda code (or layers) for different environments, so be aware that any changes made to this code will be deployed directly
to a "live" instance.
