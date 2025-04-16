import os
from app.user.models import RevokedToken
from app.utilities.models import db, ma
from config import configs
from flask import Flask, jsonify
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
from flask_migrate import Migrate
from flask import request
from flask_bcrypt import Bcrypt
from flask_cors import CORS,cross_origin

bcrypt = Bcrypt()



def create_app():
    if os.getenv("FLASK_ENV") not in ["development", "testing"]:
        """
        Prevents listing local_dev errors to sentry.
        """
    credentials_path = os.path.join(os.path.dirname(__file__), 'utilities','project-path-service-cead2e48d335.json')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path



    application = Flask(__name__)
    CORS(application)
    application.config.from_object(configs[os.getenv("SERVER_TYPE")])
    bcrypt.init_app(application)

 
    db.init_app(application)
    ma.init_app(application)

    Migrate(application, db)
    jwt = JWTManager(application)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = RevokedToken.query.filter_by(jti=jti).first()
        return token

    from app.user import user
    from app.organizations import organization
    from app.psychometrics import psychometrics
    from app.projects import projects
    from app.documents import documents
    from app.prompt import prompt


    application.register_blueprint(user)
    application.register_blueprint(organization)
    application.register_blueprint(psychometrics)
    application.register_blueprint(projects)
    application.register_blueprint(documents)
    application.register_blueprint(prompt)


    @application.route("/")
    def health_check():
        """
        Simple endpoint to ensure the server is up.
        """
        return {"status": "ok"}, 200

    @application.route("/refresh-token", methods=["POST"])
    @jwt_required(refresh=True)
    def refresh():
        """
        Endpoint for refreshing tokens
        """
        current_user = get_jwt_identity()
        ret = {"access_token": create_access_token(identity=current_user)}
        return jsonify(ret), 200

    return application


#

