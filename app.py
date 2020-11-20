import os
import sys
from random import randint
from flask import Flask, request, make_response
from flask import jsonify
import requests
import json
from datetime import datetime, timedelta, tzinfo
import DataBase as Databases

app = Flask(__name__)
database = Databases.Database()
time = 5

def registerUser(jsonstr):
    # Get new token
    uid = jsonstr.get('uid')
    hpwd = jsonstr.get('password')

    print(uid)
    if (uid is None or hpwd is None):
        user_status = 400

        jsonRaw = {
            'status': "error"
        }
    else: 
        if (len(uid) != 0 and len(hpwd) != 0):
            database.create_user(Databases.User(uid, hpwd))
            user_status = 200

            jsonRaw = {
                'status': "success"
            }
        else: 
            user_status = 400

            jsonRaw = {
                'status': "error"
            }

    jsonResponse = app.response_class(
        response=json.dumps(jsonRaw),
        status=user_status,
        mimetype='application/json'
        )
    return jsonResponse

def authenticateUser(jsonstr):
    # Connect with database
    # uid = sendMDM(jsonstr.get('email'))
    email = jsonstr.get('email')
    pwd = jsonstr.get('password')

    uid = str(sendMDM(email))

    if (uid is None or pwd is None):
        user_status = 404

        jsonRaw = {
            'status': 'error',
            'description': 'User / Password incorrect'
        }

    else:
        noPwdHash = pwd
        pwd = hashPwd(pwd)    
        print(pwd)
    
        # Error de MDM
        if (uid == "NOT_FOUND"):
            userobj = False
        else:
            userobj = database.get_user(uid)

        if userobj:
            if(userobj.password == pwd): 
                if(userobj.two_factor):
                    tokencode = str(tokenGenerate())
                    database.create_token(Databases.Token(uid, tokencode, datetime.now()))
                    user_status = 201

                    sendMailToken(tokencode, email)

                    jsonRaw = {
                        'status': 'token',
                        'uid': uid,
                    }
                else:
                    user_status = 200

                    jsonRaw = {
                        'status': 'success',
                        'uid': uid
                    }
            else: 

                tokenobj = database.get_recovery_token(uid)
                
                if tokenobj:
                    ttoken = tokenobj.date
                    tnow = datetime.now() - timedelta(minutes=time)

                    if ttoken.replace(tzinfo=None) > tnow.replace(tzinfo=None):
                
                        if( noPwdHash == tokenobj.code ):
                            database.remove_recovery_token(uid)

                            user_status = 200

                            jsonRaw = {
                                'status': 'recovery',
                                'uid': uid
                            }
                    
                        else: 
                            jsonRaw = {
                                'status': 'error',
                                'description': 'User / Password incorrect'
                            }
                            user_status = 404
                    else:
                        database.remove_recovery_token(uid)

                        jsonRaw = {
                            'status': 'expire',
                        }
                        user_status = 400
                        
                else:
                    jsonRaw = {
                        'status': 'error',
                        'description': 'User / Password incorrect'
                    }
                    user_status = 404   
                
        else:
            jsonRaw = {
                'status': 'error',
                'description': 'User / Password incorrect'
            }
            user_status = 404

    
    jsonResponse = app.response_class(
        response=json.dumps(jsonRaw),
        status=user_status,
        mimetype='application/json'
    )
    return jsonResponse

def addTokenPassword(jsonstr):
    email = jsonstr.get('email')
    uid = str(sendMDM(email))

    if (uid is None):
        user_status = 404

        jsonRaw = {
            'status': 'error',
            'description': 'Missing Arguments'
        }

    else:
        token = getHashToken()
        
        if (uid == "NOT_FOUND"):
            user_status = 404

            jsonRaw = {
                'status': 'error',
                'description': 'User Not Found'
            }
        else:
            sendMailToken(token, email)

            token = Databases.Token(uid, token)
            database.create_recovery_token(token)        

            user_status = 200

            jsonRaw = {
                'status': 'success',
            }

    jsonResponse = app.response_class(
        response=json.dumps(jsonRaw),
        status=user_status,
        mimetype='application/json'
    )

    return jsonResponse

def updatePassword(jsonstr):
    uid = jsonstr.get('email')
    newPassword = jsonstr.get('password')

    if (uid is None or newPassword is None):
        user_status = 404

        jsonRaw = {
            'status': 'error',
            'description': 'Missing Arguments'
        }
    
    else:

        uid = str(sendMDM(uid))
        tokenobj = True

        if (uid == "NOT_FOUND"):
            tokenobj = False
        
        if tokenobj:

            newPassword = hashPwd(newPassword)
            database.update_user_password(uid, newPassword)      \

            user_status = 200

            jsonRaw = {
                'status': 'success'
            }     

        else:
            user_status = 400

            jsonRaw = {
                'status': 'error',
                'description': 'Not Found'
            }

    jsonResponse = app.response_class(
        response=json.dumps(jsonRaw),
        status=user_status,
        mimetype='application/json'
    )

    return jsonResponse

def validateToken(jsonstr):
    email = jsonstr.get('correo')
    token = jsonstr.get('token')

    uid = str(sendMDM(email))

    if (uid is None or token is None):
        jsonRaw = {
                'status': 'error',
            }
        user_status = 404

    else:
        if (uid == "NOT_FOUND"):
            jsonRaw = {
                'status': 'error',
            }
            user_status = 404
        else: 

            tokenobj = database.get_token(uid)

            if tokenobj:
                ttoken = tokenobj.date
                tnow = datetime.now() - timedelta(minutes=time)

                if ttoken.replace(tzinfo=None) > tnow.replace(tzinfo=None):
                    if tokenobj.code == token:
                        jsonRaw = {
                            'status': 'success',
                        }
                        user_status = 200
                        
                        database.remove_token(uid)
                    else:
                        jsonRaw = {
                            'status': 'error',
                        }
                        user_status = 404
                else:
                    tokencode = str(tokenGenerate())
                    database.create_token(Databases.Token(uid, tokencode, datetime.now()))
                    user_status = 201

                    sendMailToken(tokencode, email)

                    jsonRaw = {
                        'status': 'expire',
                    }
                    user_status = 400
                    
            else:
                jsonRaw = {
                    'status': 'error',
                }
                user_status = 404
        
    jsonResponse = app.response_class(
        response=json.dumps(jsonRaw),
        status=user_status,
        mimetype='application/json'
    )
    return jsonResponse

def sendMDM(user):
    url = "http://35.239.19.77:8000/clients/get?correo=" + user
    print(url)
    x = requests.get(url, {})

    return x.json().get('Response')

def tokenGenerate():
    return randint(500, 99999)

def hashPwd(pwd):
    url = "https://hash-lbetwuukaq-uc.a.run.app/hash/" + pwd
    x = requests.get(url, {})

    return x.json().get('Password')

def getHashToken():
    url = "https://hash-lbetwuukaq-uc.a.run.app/otp"
    x = requests.get(url, {})

    return x.json().get('otp')

def sendMailToken( token, email ):
    url = "https://diz-marketing.herokuapp.com/TOKEN"
    x = requests.post(url, {
        'email': email,
        'password': token
    })

    print (x)

def sendMailRecovery( token, email ):
    url = "https://diz-marketing.herokuapp.com/PASSWORD"
    x = requests.post(url, {
        'email': email,
        'password': token
    })

    print (x)

@app.route('/oauth',methods=['POST'])
def authUser():
    try:
        jsonstr = request.get_json()
        return authenticateUser(jsonstr)
    except BaseException as error:
        return ('An exception occurred: {}'.format(error), 400)

@app.route('/newuser',methods=['POST'])
def newUser():
    try:
        jsonstr = request.get_json()
        return registerUser(jsonstr)
    except BaseException as error:
        return ('An exception occurred: {}'.format(error), 400)

@app.route('/recoverypassword',methods=['POST'])
def tokenpassword():
    try:
        jsonstr = request.get_json()
        return addTokenPassword(jsonstr)
    except BaseException as error:
        return ('An exception occurred: {}'.format(error), 400)

@app.route('/updatepassword',methods=['POST'])
def updatePsw():
    try:
        jsonstr = request.get_json()
        return updatePassword(jsonstr)
    except BaseException as error:
        return ('An exception occurred: {}'.format(error), 400)

@app.route('/token',methods=['POST'])
def validate():
    try:
        jsonstr = request.get_json()
        return validateToken(jsonstr)
    except BaseException as error:
        return ('An exception occurred: {}'.format(error), 400)

@app.route('/')
def home():
    return "Welcome to SSO Service"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)