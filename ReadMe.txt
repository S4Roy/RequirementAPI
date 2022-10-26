                                Please Read The Instruction From Section A To E.

****************************************** A. Admin Credential ******************************************************

    username: admin
    password: admin@123

****************************************** B. Required pip install Packages *****************************************

Flask                          2.2.2
Flask-HTTPAuth                 4.7.0
Flask-RESTful                  0.3.9
Flask-SQLAlchemy               2.5.1
Flask-WTF                      1.0.1
mysql                          0.0.3
mysql-connector-python         8.0.30
mysqlclient                    2.1.1
pytest                         7.1.3
pytest-html                    3.1.1
Werkzeug                       2.2.2

***************************************** C. Required Database Settings *********************************************

==>> Go to "connection.py" line 13-20 and  replace the below Credential Accordingly

=>username_value="root"
=>password_value="root@123"
=>host_value="127.0.0.1"
=>db_name="DBrequirmentAPI" 
one json file is avilable in project directory, replace path below if you need to test with another file
=>json_file_path_for_test="employee_and_skill_data.json"


************************************* D. About API & ENDPOINT DESCRIPTION and User Guide ****************************

The application Consist of following services:

A. external-recruitment-service
B. Internal- recruitment -service
C.Authorisation Section

The application is developd in Python/Flask with the below things in mind.

************ Description For Accessing External Requirement Services Endpoint ***************

For accessing external requirment service you don't need any authorisation Except Bring back any remove candidate
by changing there status in PUT.For that operation Admin Credential is req.

############# ENDPOINT DESCRIPTION & User Guide ###############

==>> GET   /external-recruitment-service/profile-for-skillset

HTTP Verb Is is GET
User Can send data via QUERY PARAMETER or via JSON http message body.(Both are Acceptable)
For url query parameter required_skillsets should be separated by comma(,).

EXAMPLE: required_skillsets=java,python,sql

For json data required_skillsets should be list of string.

EXAMPLE: {"required_skillsets":["java", "spring-boot", "docker", "kubernetes"]}

Expected Result: The end point return the profiles that matches the required skillset with % match.

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

Expected Result: DELETE /remove-profile mark the status of the profiles as not to be considered. Marked not be used in further 
matches and a the system will not allow such a profile to be reposted until unless admin change his status via PUT method.

EXAMPLE:

For URL query parameter cnd_Id must be an integer value ie. cnd_Id=5
For json data ie. {"cnd_Id":must_be_an_integer_value}

********** Description For Accessing Internal Requirement Services Endpoint ********************

For Accessing internal-requirements-service functionality user need Authorisation.
Admin can access internal-requirement services with his Credential(see line number 8 Section A for Credential)
Only Admin can authorised user by adding username & default password (see authentication control[line number 206 Section E]
for reference). Later user can change his password (see authentication control[line number 206 Section E]for reference).

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


************ Description For Accessing Authentication Control Endpoint *******************

Admin can add,delete & see all username by accessing the below endpoint with his Credential(see line number 5 for
Credential). Change Password can be obtain by existing users credential only.

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

ALL the verb will return succes message & Do The Appropiate task as stated in endpoint itself.



************************************ E. Instruction For Running The Application ***********************************

==>>Go to "main.py" file
==>> read the user instruction of API
==>>In project directory run cmd  "python main.py"

You Can Find localhost and port number in log file.


************************************ F. Instruction For Running Test_File *****************************************

==>> Select Default Testing Environment As pytest 
==>> change directory(cd) to "Test_Requirmrnt_API" from project directory where  "test_requirmentAPI.py" resides 
==>> Run cmd => "pytest -s test_requirmentAPI.py"
==>>For Html Report Generation Run cmd  "pytest test_requirmentAPI.py --html=report_test_requirmentAPI.html"

Or 

==>> You can run test file via Pytest TestRunner in one go

NOTE: If you want to run test_file more than once then change the candidate key because that is primary 
key otherwise it will throw error or delete database and rerun the project once, then run test file.
