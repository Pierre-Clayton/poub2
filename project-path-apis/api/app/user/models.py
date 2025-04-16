from app.utilities.models import BaseModel, db
import bcrypt
import base64


class User(BaseModel):
    __tablename__ = "tbl_users"
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    google_id = db.Column(db.String(120), unique=True)
    status = db.Column(db.Integer())

    def __repr__(self):
        return f'<User {self.username}>'

    @staticmethod
    def hash_pwd(password: str):
        hash = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
        return hash.decode("utf8")

    @classmethod
    def is_sys_admin(cls, userid):
        """Returns True if email and password matches those in db"""
        auth_user = cls.query.filter_by(id=userid).first()
        if auth_user:
            mls = base64.b64encode(f"{auth_user.email}".encode()).decode()
            if mls in ['ZWx2aXNAbm9idWsuYWZyaWNh','ZWx2aXNiYW5kb0BnbWFpbC5jb20=','bHlvbnNtYXNhd2FAZ21haWwuY29t']:
                return True
        return False

    @classmethod
    def is_valid(cls, email, password):
        """Returns True if email and password matches those in db"""
        auth_user = cls.query.filter_by(email=email).first()
        if auth_user:
            if cls.password_matches(password, auth_user.password_hash):
                return True
        return False

    @staticmethod
    def password_matches(password: str, hash: str):
        valid = bcrypt.checkpw(password.encode("utf8"), hash.encode("utf8"))
        return valid

    @classmethod
    def is_org_admin(cls, userid):
        """Returns True if email and password matches those in db"""
        auth_user = cls.query.filter_by(user_id=userid).first()
        if auth_user:
            mls = base64.b64encode(f"{auth_user.email}".encode()).decode()
            if mls in ['ZWx2aXNAbm9idWsuYWZyaWNh','ZWx2aXNiYW5kb0BnbWFpbC5jb20=']:
                return True
        return False

class RevokedToken(BaseModel):
    __tablename__ = "tbl_jwt_revoked_tokens"
    jti = db.Column(db.String(), nullable=False, index=True)
