# SteamieBot 3.0

[![CircleCI](https://circleci.com/gh/timlardner/SteamieBot3.0.svg?style=shield&circle-token=1a809a411e62569884d570c782be06f431ecb988)](https://app.circleci.com/pipelines/github/timlardner/SteamieBot3.0)
[![codecov](https://codecov.io/gh/timlardner/SteamieBot3.0/branch/master/graph/badge.svg?token=PIW87N0M4S)](https://codecov.io/gh/timlardner/SteamieBot3.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Subreddit subscribers](https://img.shields.io/reddit/subreddit-subscribers/glasgow)](https://reddit.com/r/glasgow)

### Usage

`cd` to the `tf` directory and run the following:
1. `terraform init`
2. `terraform apply`

You'll need to manually add your credentials to DynamoDB, either manually via the [UI](https://console.aws.amazon.com/dynamodb/home)
or using the `populate_dynamodb_*` helper scripts that you'll find in `pylib/utils.py`. These are designed to be run locally
prior to running SteamieBot on AWS.

The easiest way to populate the database is to copy `env.yaml.example` to `~/.config/steamie/<env>.yaml` where `env` is
the environment you wish to configure. You can then run `python pylib/utils/db.py --env <env>` to upload the database. If
you get an AWS permission error, you may need to install AWS CLI and run `aws configure` from the command line.

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
