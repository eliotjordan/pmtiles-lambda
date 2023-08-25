#!/usr/bin/env python3
import os

import aws_cdk as cdk

from pmtiles_lambda.pmtiles_lambda_stack import PmtilesLambdaStack

app = cdk.App()

PmtilesLambdaStack(
    app,
    "pmtiles-staging",
    stage="staging",
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
)

PmtilesLambdaStack(
    app,
    "pmtiles-production",
    stage="production",
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
)

app.synth()
