from app.prompt.models import RetrievalHistory
from app.documents.models import ProjectDocuments, DocumentEmbedings
from app.psychometrics.models import PsychometricScores
from app.prompt.schema import RetrievalSchema, RetrievalHistorySchema
from app.documents.schema import ProjectDocumentsSchema
from app.utilities.models import db
from flask import request, current_app
from app.utilities.resource import BaseResource
from app.utilities.awsuploads import AWSUpload
from app.utilities.embeddings import EmbedingsModel
from app.utilities.utils import UtilFunctions
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from openai import OpenAI

retieval_schema = RetrievalSchema()
retrieval_hist_schema = RetrievalHistorySchema()
retrieval_hist_list_schema = RetrievalHistorySchema(many=True)
documents_schema_many = ProjectDocumentsSchema(many=True)

aws = AWSUpload()
embeding = EmbedingsModel()
utils = UtilFunctions()


class RetrievalResource(BaseResource):
    @jwt_required()
    def get(self, id=None):
        """Returns single contact if id is included or All contacts if not set."""
        addedby = get_jwt_identity()
        if id is None:
            id = addedby    
            group = RetrievalHistory.query.filter_by(added_by=id).all()
            history = retrieval_hist_list_schema.dump(group)
        else:
            group = RetrievalHistory.query.filter_by(project_id=id, added_by = addedby).all()
            history = retrieval_hist_list_schema.dump(group)
            
        return {
                "status": 200,
                "message": "success",
                "success": True,
                "data": history}, 200

    @jwt_required()
    def post(self):
        group_json = request.get_json()
        client = OpenAI(api_key=current_app.config['OPENAI_API_KEY'])
        try:
            ret_data = retieval_schema.load(group_json)
        except Exception as e:
            return {
                "status": 400,
                "success": False,
                "message": str(e)}, 200
        userid = str(get_jwt_identity())
        projectid = str(ret_data['project_id'])
        orgid = str(ret_data['org_id'])
        emb_folder = current_app.config['DOCUMENT_EMBEDINGS']

        query_embedding = embeding.get_embedding(ret_data['prompt_text'])
        query = DocumentEmbedings.query.filter_by(project_id = projectid).order_by(
            DocumentEmbedings.embedding.cosine_distance(query_embedding)
        ).limit(5).all()
        userdata = "personality type MBTI: ISFJ - Caring, Organized, Loyal"
        docs = []
        if query:
            for doc in query:
                docs.append(doc.chunk_text)
            response = utils.ask_openai_with_context(client,ret_data['prompt_text'],userdata, docs)
            parsed = response.to_dict()
            # Extract the assistant's reply
            assistant_message = parsed['choices'][0]['message']['content']
        else:
            response = utils.ask_openai_with_context(client,ret_data['prompt_text'],userdata, "no documents")
            print(response)
            parsed = response.to_dict()
            assistant_message = parsed['choices'][0]['message']['content']
        RetrievalHistory.save_to_db({"org_id":orgid, "prompt_text": ret_data['prompt_text'],"prompt_response": assistant_message,"project_id":projectid,"added_by": userid})
        return {"status": 200, "data":assistant_message}, 200

     




        
   