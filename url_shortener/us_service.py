import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (aws_apigateway as apigateway,
                     aws_dynamodb as dynamodb,
                     aws_lambda as lambda_)

class USService(Construct):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)
        
        table =  dynamodb.Table(self, "mapping-table", 
                                partition_key=dynamodb.Attribute(
                                    name="id", 
                                    type=dynamodb.AttributeType.STRING),
                                read_capacity=10,
                                write_capacity=5)
        
        function = lambda_.Function(self, "UrlShortenerFunction",
                      code=lambda_.Code.from_asset("lambda"),
                      handler="handler.main",
                      runtime=lambda_.Runtime.PYTHON_3_9)
        
        # pass the table name to the handler through an environment variable and grant
        # the handler read/write permissions on the table.
        function.add_environment('TABLE_NAME', table.table_name)
        table.grant_read_write_data(function)

        # define the API endpoint and associate the handler
        api = apigateway.LambdaRestApi(self, "UrlShortenerApi",
                                           handler=function)