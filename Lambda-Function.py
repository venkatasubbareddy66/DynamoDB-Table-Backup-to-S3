import boto3
import json
from botocore.exceptions import ClientError
def lambda_handler(event, context):
    data = []
    TableName = "dynamodb-backup"
    try:
        s3 = boto3.resource('s3', region_name='ap-south-1')
        ddbclient = boto3.client('dynamodb', region_name='ap-south-1')
        response = ddbclient.list_tables()
        mytables = response['TableNames']
        
        if TableName in mytables:
            allitems = ddbclient.scan(TableName= TableName)
            for item in allitems['Items']:
                item_list = {}
                allKeys = item.keys()
                for k in allKeys:
                    value = list(item[k].values())[0]
                    item_list[k] = str(value)
                data.append(item_list)
            data = json.dumps(data)
            responses3 = s3.Object('dest-bucket111', 'backup_data.json').put(Body=data)
            print("Completed Upload to S3")
        print("Lambda run completed")
        return {
            'statusCode': 200,
            'body': json.dumps("success")
        }
    except ClientError as e:
        print("Detailed error: ",e)
        return {
            'statusCode': 500,
            'body': json.dumps("error")
        }
    except Exception as e:
        print("Detailed error: ",e)
        return {
            'statusCode': 500,
            'body': json.dumps("error")
        }


        // make sure you that change the bucket name , region , dynamodb TableName name 