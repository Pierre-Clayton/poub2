from datetime import datetime, timedelta
import boto3
import os
import json


class AWSUpload(object):
    """Generate PDF Report """
    def __init__(self):
        """s3 connection"""
        self.s3url = f"https://s3.amazonaws.com/projectpath-project-docs/"
        self.s3 = self.__initialize_S3()
        
    def __initialize_S3(self):
        self.session = boto3.Session(
            aws_access_key_id=os.getenv("AWSSERVERPUBLICKEY"),
            aws_secret_access_key=os.getenv("AWSSERVERSECRETKEY"))
        s3 = self.session
        return s3
        
    def list_s3_files(self, folder_name):
        # Initialize a session using Amazon S3
        s3_client = self.s3.client('s3')
        if not folder_name.endswith('/'):
            folder_name += '/'
        fscope = [a for a in self.s3url.split("/") if a != ''][-1]
        response = s3_client.list_objects_v2(
            Bucket=fscope,
            Prefix=folder_name
        )
        files = []
        # Check if the 'Contents' key is in the response dictionary
        base = 'https://s3.amazonaws.com'
        if 'Contents' in response:
            for obj in response['Contents']:
                files.append(f"{base}/{fscope}/{obj['Key']}")
                
        return files

    def upload_json_files(self,filename:str,data,deleteold=False):
        s3_client = self.s3.client('s3')
        fscope = [a for a in self.s3url.split("/") if a != ''][-1]
        bcktname = "/".join(filename.split("/")[:-1])
        if deleteold:
            try:
                response = s3_client.list_objects_v2(Bucket=fscope, Prefix=bcktname)
                for object in response['Contents']:
                    s3_client.delete_object(Bucket=fscope, Key=object['Key'])
            except:
                pass
        
        # Convert the JSON object to a string
        json_string = json.dumps(data)
        # Create a JSON file
        actlfile = os.path.basename(filename)
        with open(actlfile, 'w') as f:
            f.write(json_string)
        s3 = self.s3.resource('s3')
        s3.meta.client.upload_file(
            Filename=actlfile,
            Bucket=fscope,
            Key=filename)
        os.remove(actlfile)
        return {'file_url':f"{self.s3url}{filename}"}

    def upload_other_files(self,filename,finalname, deleteold=False):
        s3 = self.s3.resource('s3')
        s3_client = self.s3.client('s3')
        fscope = [a for a in self.s3url.split("/") if a != ''][-1]
        bcktname = "/".join(finalname.split("/")[:-1])
        if deleteold:
            try:
                response = s3_client.list_objects_v2(Bucket=fscope, Prefix=bcktname)
                for object in response['Contents']:
                    s3_client.delete_object(Bucket=fscope, Key=object['Key'])
            except:
                pass

        s3.meta.client.upload_file(
            Filename=filename,
            Bucket=fscope,
            Key=finalname)
        os.remove(filename)
        return {'file_url':f"{self.s3url}{finalname}"}

