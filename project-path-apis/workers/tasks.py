from __future__ import absolute_import
from datetime import datetime
from io import StringIO
from celery import Celery
from utils.config import BaseConfig
from utils.utils import UtilFunctions
from utils.dbmodels import ProjectDocuments,DocumentEmbedings
from utils.embeddings import EmbedingsModel
from utils.awsuploads import AWS
import os
import boto3
import numpy as np
import json
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv("utils/.env")


util = UtilFunctions()
embeding = EmbedingsModel()

celery = Celery('tasks', broker=BaseConfig.CELERY_BROKER_URL, backend=BaseConfig.CELERY_RESULT_BACKEND)
celery.conf.enable_utc = False

@celery.task(name='startembedings')
def create_embedings(data):
    s3 = AWS()
    parsed_url = urlparse(data['upload_file_raw_url'])
    bucket_name = 'projectpath-project-docs' #BaseConfig.BUCKET_NAME # Extract bucket name from the netloc part
    s3_file_path = parsed_url.path.lstrip('/')  # Extract path, removing leading slash
    fname = s3_file_path.split('/')[-1]
    orgid = s3_file_path.split('/')[-3]
    projectid = s3_file_path.split('/')[-2]
    s3_client = s3.s3.client('s3')
    # Download the file
    fileloc = f"{BaseConfig.TEMP_DOC_FOLDER}/{fname}"
    s3_client.download_file(bucket_name, f"{BaseConfig.RAW_FOLDER_NAME}/{orgid}/{projectid}/{fname}", fileloc)

    if data["file_type"] == "pdf":
        cunks = util.parse_pdf(fileloc)
        print(f"this is pdf:{cunks}")
    elif data["file_type"] == "csv":
        cunks = util.parse_csv(fileloc)
        print(f"this is here:{cunks}")
    else:
        cunks = ['nothing to add to this']
    
    print("---------- starting embdeding----------")
    embeddings = embeding.batch_get_embeddings(cunks)
    # Documents
    print("---------- completed embdeding, saving data----------")

    print(f"-------embedings shape: {embeddings.shape} -----------")
    for embed,ctext in zip(embeddings,cunks):
        tsv = {"document_id":data['document_id'],"chunk_text": ctext,"embedding":embed.tolist(),"project_id": data["project_id"]}
        util.save_to_db(DocumentEmbedings,tsv)

    # write_embeddings_to_json(embeddings,f"{fileloc}.json")
    # s3.upload_other_files(fileloc,f'{BaseConfig.EXTRACTED_FOLDER_NAME}/{orgid}/{projectid}/{fname}.json')

    #save embeddings to the data table

    return data

def write_embeddings_to_json(embeddings, file_path):
    """
    Writes embeddings to a JSON file.  Handles NumPy arrays by converting them to lists.
    Args:
        embeddings (list): A list of embeddings.  Each embedding can be a list or a NumPy array.
        file_path (str): The path to the JSON file to write.
    """
    try:
        serializable_embeddings = []
        for embedding in embeddings:
            if isinstance(embedding, np.ndarray):
                serializable_embeddings.append(embedding.tolist())  # Convert NumPy array to list
            else:
                serializable_embeddings.append(embedding) # Keep it as is
        with open(file_path, 'w') as f:
            json.dump(serializable_embeddings, f, indent=4)
        print(f"Embeddings written to '{file_path}'")
    except Exception as e:
        print(f"Error writing embeddings to JSON file: {e}")