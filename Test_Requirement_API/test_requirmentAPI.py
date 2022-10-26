'''
******************************Please go through ReadMe.txt and main.py before run the project**********************************

Select Default Testing Environment As pytest and change directory(cd) to "Test_Requirmrnt_API" from project directory 
where  "test_requirmentAPI.py" resides and Run cmd => "pytest -s test_requirmentAPI.py"
For Html Report Generation Run cmd =>"pytest test_requirmentAPI.py --html=report_test_requirmentAPI.html"

Or You can run test file via Pytest TestRunner

NOTE: If you want to run test_file more than once then change the candidate key because that is primary 
key otherwise it will throw error or delete database and rerun the project once, then run test file.
'''

import requests



# *******************************  User Control Endpoint Test ******************************************** #

########### ADMIN Control: Create User Test ###############


def test_Create_User():
    res = requests.post(
        "http://127.0.0.1:8080/users", auth=("admin", "admin@123"),json={"username": "skasif786","password":"asif@456"}
    )
    data = res.json()
    assert data["msg"] == "username added sucessfully into databases!"
    print("POST==>> Add User Control BY Admin Sucessfully RUN!")
    
    


########## Existing USER & ADMIN BOTH Control: Update User Password Test ###############


def test_update_user_password():
    res = requests.put(
        "http://127.0.0.1:8080/users/put/query", auth=("skasif786", "asif@456"),params={"update_pwd": "asif@123"}
    )
    data = res.json()
    assert data["msg"] == "password updated sucessfully into databases!"
    print("PUT==>> Password change Control BY User Sucessfully RUN!")


# *******************************  External Requirement Services Endpoint Test ********************************************* #


############ POST==>> /external-recruitment-service/post-requirement ################


def test_post_requirement_1A():
    res_post = requests.post(
        "http://127.0.0.1:8080/external-recruitment-service/post-requirement",
        json={
            
                "candidateId": 1,
                "fullname": "Joel Oram",
                "skillsets": ["java", "spring-boot", "docker", "kubernetes"],
            
        }
    )
    data = res_post.json()
    assert data["msg"] == "Data of Joel Oram added successfully for future reference!"
    print("POST==>> /external-recruitment-service/post-requirement 1A Sucessfully RUN!")


def test_post_requirement_1B():
    res_post = requests.post(
        "http://127.0.0.1:8080/external-recruitment-service/post-requirement",
        json={
            
                "candidateId": 2,
                "fullname": "Asfaq Khan",
                "skillsets": ["java", "python", "docker", "cloud"],
            
        },
    )
    data = res_post.json()
    assert data["msg"] == "Data of Asfaq Khan added successfully for future reference!"
    print("POST==>> /external-recruitment-service/post-requirement 1B Sucessfully RUN!")


############ GET   /external-recruitment-service/profile-for-skillset ################


def test_get_profile_for_skillset_2():
    res_get = requests.get(
        "http://127.0.0.1:8080/external-recruitment-service/profile-for-skillset",
        json={"required_skillsets": ["java", "spring-boot", "docker", "kubernetes"]},
    )
    data = res_get.json()

    assert int(data[0]["percentage_skillsets_match"][:-1]) > 0
    print("GET==>/external-recruitment-service/profile-for-skillset Sucessfully RUN!")


############ POST==>> /external-recruitment-service/match-requirement ################


def test_post_match_requirement_3():
    res_post = requests.post(
        "http://127.0.0.1:8080/external-recruitment-service/match-requirement",
        json={
            "requirementId": 1,
            "position": "developer",
            "requiredSkillsets": ["java", "kubernetes", "docker", "spring-boot"],
        },
    )
    data = res_post.json()

    assert data[0]["skillsets"] == sorted(
        ["java", "kubernetes", "docker", "spring-boot"]
    )
    print("POST==>> /external-recruitment-service/match-requirement Sucessfully RUN!")


############ DELETE   /external-recruitment-service/remove-profile ################


def test_delete_remove_profile_4():

    res_del = requests.delete(
        "http://127.0.0.1:8080/external-recruitment-service/remove-profile",
        params={"cnd_Id": 1},
    )
    data = res_del.json()

    assert data["msg"] == "Data Deleted Sucessfully!"
    print("Delete==>> /external-recruitment-service/remove-profile Sucessfully RUN!")


############ PUT      /external-recruitment-service/update-profile ######## Bring Back Remove Profile Control BY Admin########


def test_put_BringBackRemove_profile_5A():
    res = requests.put(
        "http://127.0.0.1:8080/external-recruitment-service/update-profile",
        auth=("admin", "admin@123"),
        json={
            
                "candidateId": 1,
                "status": True,
            
        },
    )
    data = res.json()
    assert data["msg"] == "Data Updated Sucessfully!"
    print(
        "PUT==>> /external-recruitment-service/update-profile Bring Back Remove Profile Control BY Admin Sucessfully RUN!"
    )


def test_put_update_profile_5B():
    res = requests.put(
        "http://127.0.0.1:8080/external-recruitment-service/update-profile",
        json={
            
                "candidateId": 1,
                "fullname": "Steve Smith",
            
        },
    )
    data = res.json()
    assert data["msg"] == "Data Updated Sucessfully!"
    print("PUT==>> /external-recruitment-service/update-profile Sucessfully RUN!")


# *******************************  Internal Requirement Services Endpoint Test ******************************************** #

############ POST    /internal-recruitment-service/post-requirement ==>> Control BY Authorised User and Admin BOTH ################


def test_post_requirement_6A():
    res_post = requests.post(
        "http://127.0.0.1:8080/internal-recruitment-service/post-requirement",
        auth=("skasif786", "asif@123"),
        json={
            
                "candidateId": 3,
                "fullname": "Joe Root",
                "skillsets": ["java", "spring-boot"],
            
        },
    )
    data = res_post.json()
    assert data["msg"] == "Data of Joe Root added successfully for future reference!"
    print("POST==>> /external-recruitment-service/post-requirement 6A Sucessfully RUN!")


def test_post_requirement_6B():
    res_post = requests.post(
        "http://127.0.0.1:8080/internal-recruitment-service/post-requirement",
        auth=("skasif786", "asif@123"),
        json={
            
                "candidateId": 4,
                "fullname": "Joel Oram",
                "skillsets": ["java", "python", "docker", "spring-boot"],
            
        },
    )
    data = res_post.json()
    assert data["msg"] == "Data of Joel Oram added successfully for future reference!"
    print("POST==>> /external-recruitment-service/post-requirement 6B Sucessfully RUN!")


############ POST    /internal-recruitment-service/match-requirement-optional ==>> Control BY Authorised User and Admin BOTH #####


def test_post_match_requirement_optional_7A_functionality_1():  # Return From IRS First search
    res_post = requests.post(
        "http://127.0.0.1:8080/internal-recruitment-service/match-requirement-optional",
        auth=("skasif786", "asif@123"),
        json={
            "requirementId": 1,
            "position": "developer",
            "requiredSkillsets": ["java", "spring-boot"],
            "optionalSkillsets": ["docker", "python"],
        },
    )
    data = res_post.json()

    assert data[0]["skillsets"] == sorted(["java", "python", "docker", "spring-boot"])
    print(
        "POST==>> /external-recruitment-service/match-requirement Return From IRS First search Sucessfully RUN!"
    )


def test_post_match_requirement_optional_7B_functionality_2():  # Return From IRS In 2nd Search
    res_post = requests.post(
        "http://127.0.0.1:8080/internal-recruitment-service/match-requirement-optional",
        auth=("skasif786", "asif@123"),
        json={
            "requirementId": 1,
            "position": "developer",
            "requiredSkillsets": ["java", "spring-boot"],
            "optionalSkillsets": ["docker", "cloud"],
        },
    )
    data = res_post.json()

    assert data[0]["skillsets"] == sorted(
        ["java", "spring-boot"]
    )
    print(
        "POST==>> /external-recruitment-service/match-requirement Return From IRS In 2nd Search Sucessfully RUN!"
    )


def test_post_match_requirement_optional_7C_functionality_3():  # Return From ERS In 3RD Search
    res_post = requests.post(
        "http://127.0.0.1:8080/internal-recruitment-service/match-requirement-optional",
        auth=("skasif786", "asif@123"),
        json={
            "requirementId": 1,
            "position": "developer",
            "requiredSkillsets": ["java", "python"],
            "optionalSkillsets": ["docker", "cloud"],
        },
    )
    data = res_post.json()

    assert data[0]["skillsets"] == sorted(["java", "python", "docker", "cloud"])
    print(
        "POST==>> /external-recruitment-service/match-requirement Return From ERS In 3RD Search Sucessfully RUN!"
    )
