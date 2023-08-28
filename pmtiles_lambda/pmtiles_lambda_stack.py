import os
import aws_cdk as cdk
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_s3 as s3,
    aws_apigatewayv2,
    aws_lambda,
    aws_events,
    aws_events_targets
)
from constructs import Construct

class PmtilesLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, stage: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_function = aws_lambda.DockerImageFunction(
            self,
            f"pmtiles-{stage}-PmtilesFuntion",
            code=aws_lambda.DockerImageCode.from_image_asset(
                os.path.abspath("./resources/"),
                file="Dockerfile",
                build_args={"platform" : "linux/amd64"},
                cmd=[ "handler.handler" ],
                entrypoint=["/lambda-entrypoint.sh"],
            ),
            memory_size=3008,
            timeout=Duration.seconds(600)
        )

        # S3 Permissions
        # permission = iam.PolicyStatement(
        #     actions=["s3:GetObject"],
        #     resources=[
        #         f"arn:aws:s3:::figgy-geo-{stage}/*",
        #         "arn:aws::s3:::pul-tile-images/*",
        #         "arn:aws::s3:::*/*"
        #     ]
        # )
        # lambda_function.add_to_role_policy(permission)
        # role = iam.Role( self, "Role", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        # Add function url to primary lambda
        # Use instead of API gateway to bypass 30 second gateway timeout limit
        lambda_url = lambda_function.add_function_url(
            auth_type=aws_lambda.FunctionUrlAuthType.NONE
        )
        function_url = cdk.Fn.select(2, cdk.Fn.split('/', lambda_url.url))

        cdk.CfnOutput(self, "Function URL", value=function_url)

