"""
******************************Please go through ReadMe.txt and main.py before run the project**********************************

This Module contains  User Table Details, Resources Class For Implement The CRUD Operation in USER Table  and Implementation
Of USER ACCESS AUTHORISATION.

HTTP Basic AUTHENTICATION Implementation

"""


from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from connection import *


admin_auth = HTTPBasicAuth()
user_auth = HTTPBasicAuth()


class UserTBL(db.Model):
    username = db.Column(db.String(100), primary_key=True, nullable=False)
    password = db.Column(db.String(200), nullable=False, default="NA")


class UserAccess(Resource):

    method_decorators = {
        "put": [user_auth.login_required],
        "post": [admin_auth.login_required],
        "get": [admin_auth.login_required],
        "delete": [admin_auth.login_required],
    }

    def get(self):
        all_user = UserTBL.query.all()
        value = {"All_Username": []}
        i = 1
        for item in all_user:
            value["All_Username"].append({f"User: {i}": item.username})
            i += 1
        if value["All_Username"]:
            return value
        return {"msg": "There Is No User Into Database!"}, 404

    def post(self):  # information pass by http message body

        try:
            data = request.get_json()
            given_username = data["username"]
            given_password = data["password"]
        except:
            return {
                "msg": "please put username password in json format in http msg body!"
            }, 404

        if not UserTBL.query.filter_by(username=given_username).all():
            current_item = UserTBL(
                username=given_username, password=generate_password_hash(given_password)
            )
            db.session.add(current_item)
            db.session.commit()
            return {"msg": "username added sucessfully into databases!"}
        return {"msg": "username already exist!"}, 404

    def put(self, update_pwd="NA"):  # information pass by http message body

        if update_pwd == "NA":  # this part is for query passing throuh
            args = request.args
            if args.get("update_pwd"):
                given_username = request.authorization.username
                given_password = args["update_pwd"]
            else:
                return {
                    "msg": "please enter update password in optional query part of url.eg: /query?update_pwd=asif@123"
                }, 404
        else:
            given_username = request.authorization.username
            given_password = update_pwd
        current_item = UserTBL.query.filter_by(username=given_username).first()
        if current_item:  # check condition for re run script
            current_item.password = generate_password_hash(given_password)
            db.session.commit()
            return {"msg": "password updated sucessfully into databases!"}
        return {"msg": "username does not exist !"}, 404

    def delete(self, name="NA"):
        if name == "NA":  # this part is for query passing throuh
            args = request.args
            if args.get("username"):
                given_username = args["username"]
            else:
                return {
                    "msg": "please enter username in optional query part of url.eg: username=asif"
                }, 404
        else:
            given_username = name

        current_item = UserTBL.query.filter_by(username=given_username).first()
        if current_item:
            db.session.delete(current_item)
            db.session.commit()
            return {
                "msg": f"Username: {given_username} Deleted successfully from Databases!"
            }
        return {"msg": "Username not found in db!"}, 404


@user_auth.verify_password
def User_authentication(username, password):
    if Admin_authentication(
        username, password
    ):  # Checking If Admin Is Accessing or Not
        return True

    current_item = UserTBL.query.filter_by(username=username).first()
    if current_item and check_password_hash(current_item.password, password):
        return True
    return False


@admin_auth.verify_password
def Admin_authentication(username, password):
    if username == "admin" and password == "admin@123":
        return True
    return False
