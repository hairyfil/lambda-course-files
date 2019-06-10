import boto3
from wand.image import Image
import json
import os


s3 = boto3.client('s3')


def lambda_handler(event, context):
    bucketname=(event["Records"][0]["s3"]["bucket"]["name"])
    key= (event["Records"][0]["s3"]["object"]["key"])
    
    print(event["Records"][0]["s3"]["bucket"]["name"])
    print ("my incoming bucketname = ", bucketname)
    print ("my incoming key = ", key)

    with open('/tmp/image.jpg', 'wb') as data:
        s3.download_fileobj(bucketname, key, data)

    with Image(filename='/tmp/image.jpg') as img:
        print('width =', img.width)
        print('height =', img.height)
        img.resize(200, 200)

        #this will save the resized file
        img.save(filename='/tmp/image.jpg')


    resizeName="resized-"+key
    upload = boto3.resource('s3')
    uploadbucketname = bucketname+"-resized100"

    print("my uploadbucketname = ", uploadbucketname)
    print("my resizename = ", resizeName)
    print("uploading the resized image...")
    
    try:
        upload.Object(uploadbucketname, resizeName).upload_file('/tmp/image.jpg')
        print("uploading succeeded")
    except Exception as e:
        print ("uploading failed")
        print ("%s", e)
    
