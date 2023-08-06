import os
import json
import optparse

parser = optparse.OptionParser()

parser.add_option('-r', '--role-name',action="store", dest="rolename",help="your role name", default="autoCheck")
parser.add_option('-f', '--function-name',action="store", dest="functionname",help="your funtion name", default="getWhirldataClient")
parser.add_option('-a', '--api-name',action="store", dest="apiname",help="your api name", default="whirldataClient")
parser.add_option('-b', '--s3-bucket-name',action="store", dest="bucketname",help="your s3 bucket name", default="whirldataclient")
parser.add_option('-k', '--s3-key-name',action="store", dest="keyname",help="your s3 bucket key name end with .zip", default="AcceleratorV3-21Dec2017-3pm.zip")
parser.add_option('-s', '--stage-name',action="store", dest="stagename",help="your stage name", default="whirldataClient")
parser.add_option('-u', '--url',action="store", dest="url",help="your project zip url", default="https://s3.amazonaws.com/whirlbot-accl/AcceleratorV3-21Dec2017-3pm.zip")
parser.add_option('-g', '--region',action="store", dest="region",help="your region", default="us-east-1")

options, args = parser.parse_args()


role_name = options.rolename
function_name = options.functionname
api_name = options.apiname
s3_bucket_name = options.bucketname
s3_key_name = options.keyname
stage_name = options.stagename
url = options.url
region = options.region
s3_bucket_name = "whirldata-"+s3_bucket_name

print("Download URL="+url)
print("Region="+region)
print("Role Name="+role_name)
print("Lambda Function Name="+function_name)
print("API Name="+api_name)
print("S3 Bucket Name="+s3_bucket_name)
print("S3 Key Name="+s3_key_name)
print("Deployment State Name="+stage_name)


zip_file = url.rsplit('/', 1)[-1]
if(not os.path.exists(zip_file)):
  print("[INFO] Downloading Project ZIP")
  os.system("curl -O "+url)


print("[INFO] Creating Bucket name as {}".format(s3_bucket_name))
os.system("aws s3api create-bucket --region "+region+" --bucket "+s3_bucket_name+" > bucket.json")
print("[INFO] Creating key name as {}".format(s3_key_name))
os.system("aws s3api put-object --region "+region+" --bucket "+s3_bucket_name+" --key "+s3_key_name+" --body ./"+zip_file+" > test.json")

print("[INFO] Creating role as name {}".format(role_name))
os.system("aws iam create-role --region "+region+" --role-name "+role_name+" --assume-role-policy-document file://lambda.json > role.json")
with open('role.json', 'r') as f:
  role_json = json.load(f)

print("[INFO] Assume Policy to your role")

os.system("aws iam attach-role-policy --region "+region+" --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess --role-name "+role_name)
os.system("aws iam attach-role-policy --region "+region+" --policy-arn arn:aws:iam::aws:policy/AmazonAPIGatewayInvokeFullAccess --role-name "+role_name)
os.system("aws iam attach-role-policy --region "+region+" --policy-arn arn:aws:iam::aws:policy/AmazonLexFullAccess --role-name "+role_name)
os.system("aws iam attach-role-policy --region "+region+" --policy-arn arn:aws:iam::aws:policy/AWSLambdaFullAccess --role-name "+role_name)

#os.system("aws lambda create-function --function-name "+function_name+" --runtime java8 --role "+role_json['Role']['Arn']+" --handler com.AcceleratorEventHandler --zip-file fileb://AcceleratorV3-21Dec2017-3pm.zip --environment Variables={isInitialize=no} --timeout 30 --memory-size 512 --description 'This is test lambda creation using aws cli' > lambdafunction.json")
print("[INFO] Creating Lambda Function")
os.system("aws lambda create-function --region "+region+" --function-name "+function_name+"  --code S3Bucket="+s3_bucket_name+",S3Key="+s3_key_name+" --role "+role_json['Role']['Arn']+" --handler com.AcceleratorEventHandler --runtime java8 --environment Variables={isInitialize=no,dbRegion="+region+"} --timeout 30 --memory-size 512 --description 'This is test lambda creation using aws cli' > lambda_function.json")


with open('lambda_function.json') as lf:
  lambda_function = json.load(lf)

print(lambda_function)

print("[INFO] Creating Rest Api")
os.system("aws apigateway create-rest-api --region "+region+" --name "+api_name+" --description 'This is AWS CLI' > api.json")
with open('api.json') as api:
  api_json = json.load(api)



print("[INFO] Getting Resource ID")
os.system('aws apigateway get-resources --region '+region+' --rest-api-id '+api_json["id"]+' > resource.json')

with open('resource.json') as resource:
  resource_json = json.load(resource)



print("[INFO] Creating Method Request")
os.system("aws apigateway put-method --region "+region+" --rest-api-id "+api_json['id']+" --resource-id "+resource_json['items'][0]['id']+" --http-method POST --authorization-type NONE --request-models '{\"application/json\": \"Empty\"}' > test.json")

print("[INFO] Creating Method Responce")
os.system("aws apigateway put-method-response --region "+region+" --rest-api-id "+api_json['id']+" --resource-id "+resource_json['items'][0]['id']+" --http-method POST --status-code 200 --response-models '{\"application/json\": \"Empty\"}' > test.json")

print("[INFO] Creating Integration Request")
os.system("aws apigateway put-integration --region "+region+" --rest-api-id "+api_json['id']+" --resource-id "+resource_json['items'][0]['id']+" --http-method POST --type AWS_PROXY --integration-http-method POST --uri arn:aws:apigateway:"+region+":lambda:path/2015-03-31/functions/"+lambda_function['FunctionArn']+"/invocations > test.json")

print("[INFO] Deployment to your API")
os.system("aws apigateway create-deployment --region "+region+" --rest-api-id "+api_json['id']+" --stage-name "+stage_name+" --stage-description 'Whirldata Client Stage' > test.json")

print("[INFO] Adding Trigger to Lambda Function")
print(lambda_function['FunctionArn'].split(":")[4])
os.system("aws lambda add-permission --region "+region+" --function-name "+function_name+" --statement-id apigateway-whirldata-client --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn arn:aws:execute-api:"+region+":"+lambda_function['FunctionArn'].split(":")[4]+":"+api_json['id']+"/*/POST/ > test.json")

print("[INFO] Your API url is")
print("https://"+api_json['id']+".execute-api."+region+".amazonaws.com/"+stage_name+"/")


