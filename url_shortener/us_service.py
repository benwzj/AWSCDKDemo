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
        
        # pass the table name to the handler through an environment variable 
        # There are a key point which need to be understood here: When we execute 
        # CDK app, what is really doing is creating this desired state representation,  
        # this model of what we want in our infrastructure to look like.
        # We are not actually provisioning the infrastructure when we run this app.
        # 
        # So at this point when the code run, the table isn't created, 
        # we actually don't know what that table name is.
        # What actually happen underneath the cover here is we are using the 
        # token system in the CDK, and tokens allow us to do this late bindng at
        # provisioning time. So even we don't know what is the table name, 
        # when this code is run, we gonna output in our desired state. 
        # This kind of Ford reference that allow it to be resolved at the 
        # provisioning time and we end up with exactly what we expect. 
        function.add_environment('TABLE_NAME', table.table_name)

        # grant the handler read/write permissions on the table.  
        # Here will create IAM role, policy, etc. They need table name as well      
        table.grant_read_write_data(function)

        # define the API endpoint and associate the handler
        api = apigateway.LambdaRestApi(self, "UrlShortenerApi",
                                           handler=function)
        