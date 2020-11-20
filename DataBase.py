from google.cloud import firestore
import google.cloud.exceptions
from datetime import datetime, timedelta


class User:

    # Create new User
    # @param uid {string} - User ID
    # @param password {string} - Hashing Password
    # @param {boolean} [two_factor=True] - Enable two factor authentication
    def __init__(self, uid, password, two_factor=True):
        self.uid = uid
        self.password = password
        self.two_factor = two_factor

    def __repr__(self):
        return (
            f'(UID: {self.uid}, '
            f'password: {self.password}, '
            f'twoFactor: {self.two_factor})'
        )


class Token:

    # Create new Token
    # @param uid {string} - User ID
    # @param code {string} - Token code
    # @param {datetime} [date=datetime.now()] - Date of creation
    def __init__(self, uid, code, date=datetime.now()):
        self.uid = uid
        self.code = code
        self.date = date

    def __repr__(self):
        return (
            f'(UID: {self.uid}, '
            f'code: {self.code}, '
            f'date: {self.date.strftime("%X")})'
        )


class Database(object):

    def __init__(self):
        self.user_db = firestore.Client().collection(u'users')
        self.token_db = firestore.Client().collection(u'tokens')
        self.recovery_token_db = firestore.Client().collection(u'recovery_token')

    # Upload a new User
    # @param user {Object} - User Object
    # @return {boolean} - Success
    def create_user(self, obj):
        doc_ref = self.user_db.document(obj.uid)
        doc_ref.set({
            u'uid': obj.uid,
            u'password': obj.password,
            u'two_factor': obj.two_factor
        })
        return True

    # Upload a user password
    # @param uid {string} - User id
    # @param password {string} - New hashing password
    # @return {boolean} - Success
    def update_user_password(self, uid, password):
        doc_ref = self.user_db.document(uid)
        doc_ref.update({
            u'password': password
        })
        return True

    # Get User
    # @param uid {string} - User id
    # @return {Object} - User Object
    # @throws Will trows False if the user doesn't exist
    def get_user(self, uid):
        doc_ref = self.user_db.document(uid)

        try:
            usr_dic = doc_ref.get()

            if usr_dic.exists:
                usr_dic = usr_dic.to_dict()
                user = User(usr_dic["uid"], usr_dic["password"], usr_dic["two_factor"])
                return user
            else:
                return False               

        except google.cloud.exceptions.NotFound:
            return False

    # Upload / Create a new Token
    # @param token {Object} - Token Object
    # @return {boolean} - Success
    def create_token(self, obj):
        doc_ref = self.token_db.document(obj.uid)
        doc_ref.set({
            u'code': obj.code,
            u'date': obj.date
        })
        return True

    # Get Token
    # @param uid {string} - User id
    # @return {Object} - Token Object
    # @throws Will trows False if the token doesn't exist
    def get_token(self, uid):
        doc_ref = self.token_db.document(uid)

        try:
            token_dic = doc_ref.get()

            if token_dic.exists:
                token_dic = token_dic.to_dict()
                token = Token(uid, token_dic["code"], token_dic["date"])

                return token
            else:
                return False

        except google.cloud.exceptions.NotFound:
            return False

    # Remove Token
    # @param uid {string} - User id
    # @return {boolean} - Success
    def remove_token(self, uid):
        self.token_db.document(uid).delete()
        return True

    # Remove expired Tokens
    # @return {boolean} - Success
    def remove_expired_tokens(self):
        docs = self.token_db.where(u'date', u"<", datetime.now() - timedelta(minutes=1)).stream()

        for doc in docs:
            self.remove_token(doc.id)

        return True

    # Upload / Create a new Recovery Token
    # @param token {Object} - Token Object
    # @return {boolean} - Success
    def create_recovery_token(self, obj):
        doc_ref = self.recovery_token_db.document(obj.uid)
        doc_ref.set({
            u'code': obj.code,
            u'date': obj.date
        })
        return True

    # Get Recovery Token
    # @param uid {string} - User id
    # @return {Object} - Token Object
    # @throws Will trows False if the recovery token doesn't exist
    def get_recovery_token(self, uid):
        doc_ref = self.recovery_token_db.document(uid)

        try:
            token_dic = doc_ref.get()

            if token_dic.exists:
                token_dic = token_dic.to_dict()
                return Token(uid, token_dic["code"], token_dic["date"])

            else:
                return False
        except google.cloud.exceptions.NotFound:
            return False

    # Remove Recovery Token
    # @param uid {string} - User id
    # @return {boolean} - Success
    def remove_recovery_token(self, uid):
        self.recovery_token_db.document(uid).delete()
        return True

    # Remove expired recovery Tokens
    # @return {boolean} - Success
    def remove_expired_recovery_tokens(self):
        docs = self.recovery_token_db.where(u'date', u"<", datetime.now() - timedelta(minutes=1)).stream()

        for doc in docs:
            self.remove_token(doc.id)

        return True