
from app.utilities.resource import BaseResource
from flask_jwt_extended import jwt_required


class PsychometricsTypesResource(BaseResource):
    @jwt_required()
    def get(self):
        tests = {
            "BFI-10": {"name":"Big Five Index","questions": 10, "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            "BFI-20": {"name":"Big Five Index","questions": 20, "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            "BFI-40": {"name":"Big Five Index","questions": 40, "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            "MBTI-12": {"name": "Myers-Brigs Type Indicator", "questions": 12, "options": ["Agree", "Disagree"]},
            "MBTI-20": {"name": "Myers-Brigs Type Indicator", "questions": 20, "options": ["Agree", "Disagree"]},
            "MBTI-25" : {"name": "Myers-Brigs Type Indicator", "questions": 25, "options": ["Agree", "Disagree"]}

            }


        return tests
        
   