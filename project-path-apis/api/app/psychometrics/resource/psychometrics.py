from app.psychometrics.models import PsychometricScores
from app.psychometrics.schema import PsychometricScoresSchema, PsychometricPostSchema
from app.utilities.models import db
from flask import request
from app.utilities.resource import BaseResource
from app.utilities.psychotests import bfi_index, mbti_index, mbti_full
from flask_jwt_extended import jwt_required
import json

psychom_schema = PsychometricScoresSchema()
response_post_schema = PsychometricPostSchema()

class PsychometricsResource(BaseResource):
    @jwt_required()
    def get(self, id=None):
        """Returns single contact if id is included or All contacts if not set."""
        args = dict(request.args)
        if id is None:
            if 'type'  in args:
                testyype = "".join(filter(str.isalpha,args['type']))
                if testyype == "BFI":
                    data = bfi_index(args['type'])
                    return {
                        "status": 200,
                        "message": "success",
                        "success": True,
                        "data": data
                    }, 200
                elif testyype == "MBTI":
                    data = mbti_index(args['type'])
                    return {
                        "status": 200,
                        "message": "success",
                        "success": True,
                        "data": data
                    }, 200
            else:
                return {
                    "status": 500,
                    "message": "pass the psychometric type",
                    "success": False
                }, 200
     
        group = PsychometricScores.query.filter_by(user_id=id).first()
        if group:
            group_data = psychom_schema.dump(group)
            try:
                mbti_scores = json.loads(group_data['mbti_scores'])
            except:
                mbti_scores = None
            try:
                bfi_scores = json.loads(group_data['bfi_scores'])
            except:
                bfi_scores = None

            return {
                "status": 200,
                "message": "success",
                "success": True,
                "data": group_data}, 200
        else:
            if 'type'  in args:
                if args['type'].startswith("BFI"):
                    data = bfi_index(args['type'])
                    return {
                        "status": 200,
                        "message": "success",
                        "success": True,
                        "data": data
                    }, 200
                elif args['type'].startswith("MBTI"):
                    data = mbti_index(args['type'])
                    return {
                        "status": 200,
                        "message": "success",
                        "success": True,
                        "data": data
                    }, 200
            else:
                return {
                    "status": 500,
                    "message": "pass the psychometric type",
                    "success": False
                }, 200



    @jwt_required()
    def post(self):
        group_json = request.get_json()
        try:
            psycho_data = response_post_schema.load(group_json)
        except Exception as e:
            return {
                "status": 400,
                "success": False,
                "message": str(e)}, 200
        testyype = "".join(filter(str.isalpha,psycho_data['test_type']))
        
        if testyype == "BFI":
            tquest = bfi_index(psycho_data['test_type'])
            trait_totals = {trait: 0 for trait in ["Extraversion", "Agreeableness", "Conscientiousness", "Neuroticism", "Openness"]}
            trait_counts = {trait: 0 for trait in trait_totals}
            for resp in psycho_data['questions']:
                score_map = {"Strongly Disagree": 1, "Disagree": 2, "Neutral": 3, "Agree": 4, "Strongly Agree": 5}
                mp = [a for a in tquest if a['question'] == resp['question']][0]
                score = 6 - score_map[resp['response']] if mp['reverse'] else score_map[resp['response']]
                trait_totals[mp['trait']] += score
                trait_counts[mp['trait']] += 1

            bfi_score = {trait: round(trait_totals[trait] / trait_counts[trait], 2) for trait in trait_totals}
            ans = {"user_id": str(psycho_data['user_id']), "bfi_scores": json.dumps(bfi_score),"bfi_type": ""}
        
        elif testyype == "MBTI":
            tquest = mbti_full()
            mbti_scores = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
            score_map = {"Disagree": 0, "Agree": 1}
            for resp in psycho_data['questions']:  # assuming 10 MBTI questions are shown
                dimension = [a['trait'] for a in tquest if a['question'] == resp['question']][0]
                score = score_map[resp['response']]
                mbti_scores[dimension] += score
            mbti_type = ''.join([
                'E' if mbti_scores['E'] >= mbti_scores['I'] else 'I',
                'S' if mbti_scores['S'] >= mbti_scores['N'] else 'N',
                'T' if mbti_scores['T'] >= mbti_scores['F'] else 'F',
                'J' if mbti_scores['J'] >= mbti_scores['P'] else 'P'
            ])

            ans = {"user_id": str(psycho_data['user_id']), "mbti_scores": json.dumps(mbti_scores),"mbti_type": mbti_type}

        personalscore = PsychometricScores.query.filter_by(user_id = str(psycho_data['user_id'])).first()
        if personalscore:
            fieldstoupdate = ["mbti_scores","mbti_type"] if testyype == "MBTI" else ["bfi_scores","bfi_type"]
            for field in fieldstoupdate:
                setattr(personalscore, field, ans[field])
            PsychometricScores.update_record()
        else:
            try:
                PsychometricScores.save_to_db(ans)
            except Exception as e:
                db.session.rollback()
                return {
                    "status": 400,
                    "success": False,
                    "message": f'error encountered - {e}'}, 200
        return {"success": True, "message": "successfully added score", "status": 201, "data":ans }, 200


        
   