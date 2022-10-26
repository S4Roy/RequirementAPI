"""
******************************Please go through ReadMe.txt and main.py before run the project**********************************


This module contains all path and details of accessing the endpoint
Also this module have all the function run cmd and the main method for run the application.


**** HTTP Basic Authentication Details ***

    Admin Credential
    
        username: admin
        password: admin@123
    
    
NOTE:    Admin Credential Neither Be Change Nor Be Destroyed: See "authentication.py" module line number 122 For reference.

"""


from external_and_internal_RequirementService import *


# For Creation Of Table Running Below Line Once is Enough.

db.create_all()


# For Adding Item Into Database From JSON File present in current Directory (Testing Purpose) Running below Line Once is Enough.
# Testing purpose only,You can comment this line and run the test script also for testing
add_item_in_db_for_testing_api()


# $$$$$$$$$$$$ Path For accessing The External-Requirement Service Resources According To The Project Specification PDF $$$$$$$$$$

api.add_resource(
    ersFirst,
    "/external-recruitment-service/profile-for-skillset",
    "/external-recruitment-service/post-requirement",
    "/external-recruitment-service/update-profile",
    "/external-recruitment-service/remove-profile",
)
api.add_resource(ersSecond, "/external-recruitment-service/match-requirement")

"""
********************* Description For Accessing External Requirement Services Endpoint *********************

For accessing external requirment service you don't need any authorisation Except Bring back any remove candidate by changing 
there status in PUT.For that operation Admin Credential IS req.

############# ENDPOINT DESCRIPTION & User Guide ###############

==>> GET   /external-recruitment-service/profile-for-skillset

HTTP Verb Is is GET
User Can send data via QUERY PARAMETER or via JSON http message body.(Both are Acceptable)
For url query parameter required_skillsets should be separated by comma(,).

EXAMPLE: required_skillsets=java,python,sql

For json data required_skillsets should be list of string.

EXAMPLE: {"required_skillsets":["java", "spring-boot", "docker", "kubernetes"]}

==>>POST    /external-recruitment-service/post-requirement

HTTP Verb Is is POST
USER Can send data via  JSON in HTTP msg body.
Candidate ID should Be Unique In This Case If not then output will be an error msg with last_added_CandidateID.

EXAMPLE:
        
{
"candidateId": 1,
"fullname": "Joel Oram",
"skillsets": ["java", "spring-boot", "docker", "kubernetes"]
}

Expected Result: Store the given input in a database for later reference. Respond
            with a success msg.

==>>POST    /external-recruitment-service/match-requirement

HTTP Verb Is POST
USER Can send data via  JSON in HTTP msg body.

EXAMPLE:


{
"requirementId": 1,
"position": "developer",
"requiredSkillsets": [ "java", "kubernetes", "docker", "spring-boot" ]
}

Expected Result: Match the required Skillsets with the available skillsets in the
data store / database and return candidates who match the skillsets.

Response:
[
{
"candidateId": 1,
"fullname": "Joel Oram",
"skillsets": [ "java", "spring-boot", "docker", "kubernetes" ]
}
]

==>> PUT      /external-recruitment-service/update-profile

HTTP Verb Is PUT
USER Can send data via  JSON in HTTP msg body.Providing candidateId is Mandatory & Can't Be Updated.
The end point update the profile and return a success msg.
       
EXAMPLE:

{
"candidateId": 1,
"fullname": "Joel Oram",
"skillsets": [ "java", "spring-boot", "docker", "kubernetes" ]
}

Expected Result: Update the given input in a database for later reference. Respond
with success msg.

NOTE: If one candidate is remove, then only admin can bring that candidate back by sending his LOGIN CREDENTIAL with request.
Only for bring any Remove candidate back user need to provide "status=true" in json data and Admin credential as HTTP 
basic authorisation data.

==>>DELETE   /external-recruitment-service/remove-profile

HTTP Verb Is DELETE
You can send the cnd_Id via query parameter or via json file.(Both acceptable)
DELETE /remove-profile mark the status of the profiles as not to be considered. Marked not be used in further 
matches and a the system will not allow such a profile to be reposted until unless admin change his status via PUT method.

EXAMPLE:

For URL query parameter cnd_Id must be an integer value ie. cnd_Id=5
For json data ie. {"cnd_Id":must_be_an_integer_value}

"""


# $$$$$$$$$$$ Path For accessing The Internal-Requirement Service Resources According To The Project Specification PDF $$$$$$$$$$$$

api.add_resource(irsFirst, "/internal-recruitment-service/post-requirement")
api.add_resource(irsSecond, "/internal-recruitment-service/match-requirement-optional")

"""
********************* Description For Accessing Internal Requirement Services Endpoint *********************

For Accessing internal-requirements-service functionality user need Authorisation.
Admin can access internal-requirement services with his Credential(see line number 8 for Credential)
Only Admin can authorised user by adding username & default password (see authentication control[line number 218 ]for reference).
Later user can change his password (see authentication control[line number 242]for reference).

############# ENDPOINT DESCRIPTION & User Guide ###############

==>>POST    /internal-recruitment-service/post-requirement

HTTP verb is POST.
You Can send data via  JSON in HTTP msg body.CandidateId should Be Unique In This Case.

EXAMPLE:

{
"candidateId": 1,
"fullname": "Joel Oram",
"skillsets": [ "java", "spring-boot", "docker", "kubernetes" ]
}

Expected Result: Store the given input in a database for later reference. Respond
with success messages.


==>>POST    /internal-recruitment-service/match-requirement-optional

HTTP verb is POST.
You Can send data via  JSON in HTTP msg body.CandidateId should Be Unique In This Case.

EXAMPLE:
{
"requirementId": 1,
"position": "developer",
"requiredSkillsets": [ "java", "spring-boot" ],
"optionalSkillsets": [ "docker", "kubernetes" ]
}

Expected Result:

Match the required Skillsets and optional Skillsets with the available skillsets in the
data store / database within the internal recruitment service and return back if such a
candidate exists.

If there are no candidates in the first check then match with the required SkillSets alone with
the available skillsets (by leaving out the Optional Skillsets) and return back if such a
candidate exists

If both the match operations above do not return a candidate then call the external-hiring-
service to get the candidates that match both the required Skillsets and optional
Skillsets and return the candidates with matching skillsets.

• Respond with the list of candidates as below.

[
{
"candidateId": 1,
"fullname": "Joel Oram",
"skillsets": [ "java", "spring-boot", "docker", "kubernetes" ]
}
]
        
"""


# $$$$$$$$$$$$$$$$$$$$$$$$$ Path For Authentication Control According To Developer Assumption $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


api.add_resource(
    UserAccess,
    "/users",
    "/users/add",
    "/users/delete/query",
    "/users/delete/<string:name>",
    "/users/put/query",
    "/users/put/<string:update_pwd>",
)

"""
************************************** Description For Accessing Authentication Control Endpoint *****************************************************

Admin can add,delete & see all username by accessing the below endpoint with his Credential(see line number 8 for Credential).
Change Password can be obtain by existing users credential only.

############# ENDPOINT DESCRIPTION & User Guide ###############

==>>     /users

HTTP Verb Is GET
This end point will return all the username list which are added into database.

==>>    /users/add

HTTP Verb Is POST
Information pass by http message body.

EXAMPLE:

{
    "username":"skasif786",
    "password":"asif@123"
}

==>>    /users/delete/query     OR        /users/delete/<string:name>

HTTP Verb Is DELETE
Information pass by http message query parameter or by directly /users/username_that_need_to_deleted

EXAMPLE:

/users/delete/query?username=skasif786
OR
/users/delete/skasif786


==>>    /users/put/query  OR   /users/put/<string:update_pwd>

HTTP Verb Is PUT
A user with his existing credential can access this path for update their default password.
Information pass by http message query parameter or by directly /users/password_that_want_to_be_update.

EXAMPLE:

/users/put/query?update_pwd=asif@456

OR

/users/delete/asif@456

ALL the verb will return succes message.

"""
@app.route("/home")
def get_all():
    m={'internal':[],'external':[]}
    items=ersTBL.query.all()
    for item in items:
        m['external'].append({"candidateId":item.candidateId,"skill":item.skillsets})
    items=irsTBL.query.all()
    for item in items:
        m['internal'].append({"candidateId":item.candidateId,"skill":item.skillsets})
    return jsonify(m)
        

# Driver Code: Main Method
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True, use_reloader=False)
