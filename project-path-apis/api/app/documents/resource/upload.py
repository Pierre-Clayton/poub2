from flask import request, current_app
from app.documents.schema import UploadPostSchema
from app.documents.models import ProjectDocuments
from app.utilities.resource import BaseResource
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from datetime import datetime
from marshmallow import ValidationError
from werkzeug.utils import secure_filename
from celery import Celery
from PyPDF2 import PdfReader
import os
import tempfile
from app.utilities.awsuploads import AWSUpload

statement_schema = UploadPostSchema()
aws = AWSUpload()

class UploadDocumentsResource(BaseResource):    
    def __init__(self):
        """GCP bucket connection"""
        self.raw_folder_name = current_app.config['RAW_DOCUMENTS']
        self.extracted_folder_name = current_app.config['DOCUMENT_EMBEDINGS']
        self.celery = Celery(
            'tasks', broker=current_app.config['CELERY_BROKER_URL'],
            backend=current_app.config['CELERY_RESULT_BACKEND'])

    @jwt_required()
    def post(self):
        file = request.files['uploaded_file']
        # ensure that a file was selected
        if not file:
            return 'No file selected', 400

        file_data = {'uploaded_file': file, 'project_id': request.form.get(
                'project_id'), 'file_password': request.form.get('file_password'),'org_id': request.form.get(
                'org_id')}
        try:
            statement_schema.load(file_data)
        except ValidationError as err:
            return {"status":400, "success":False, "message": f"{err.messages}"}, 200
        
        randomstr = str(int(datetime.now().timestamp()))
        initfilename = file.filename
        filename = secure_filename(file.filename)        
        id = str(file_data['project_id'])
        orgid = str(file_data['org_id'])
        finalname = f"/{orgid}/{id}/{randomstr}{filename}"
        finalname = finalname.lower()    
        f = os.path.join(current_app.config['UPLOAD_FOLDER'], f"{randomstr}{filename}")
        file.save(f)
        file.seek(0)
        if file.filename.endswith('.pdf'):
            # validate the description field using the schema
            try:
                with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
                    temp_pdf.write(file.read())
                reader = PdfReader(temp_pdf.name)
                if reader.is_encrypted:
                    if (reader.decrypt(file_data['file_password']) == 0):
                        return {"message":'Invalid password', "status": 400}, 200
            except Exception as e:
                return str(e), 400

        urls = aws.upload_other_files(f,f"{self.raw_folder_name}{finalname}")
        
        savedata = {
                "org_id":orgid,
                "project_id":id,
                "upload_file_name": initfilename,
                "upload_file_type": initfilename.split(".")[-1],
                "upload_file_raw_url": urls['file_url'],
                "file_password": file_data['file_password'],
                "added_by": str(get_jwt_identity())
            } 

        doc = ProjectDocuments.save_to_db(savedata)

        self.celery.send_task(
            'startembedings', args=[{"document_id": str(doc.id),"project_id": str(doc.project_id),"file_type": savedata['upload_file_type'], "upload_file_raw_url": savedata['upload_file_raw_url']}], kwargs={}, expires=2400)
    
        return {"status": 201,
                "message": "document uploaded",
                "success": True,
                "data": savedata
                }, 201

    