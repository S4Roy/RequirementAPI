"""
******************************Please go through ReadMe.txt and main.py before run the project**********************************

This Module contains All The Table Details and Resources Class For Implement The CRUD Operation
"""

from authentication import *
from my_logger import *
from connection import *


from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType


class ersTBL(db.Model):
    candidateId = db.Column(db.Integer, primary_key=True, nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=True)
    skillsets = db.Column(MutableList.as_mutable(PickleType), default=[])


class irsTBL(db.Model):
    candidateId = db.Column(db.Integer, primary_key=True, nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=True)
    skillsets = db.Column(MutableList.as_mutable(PickleType), default=[])


# This function will add data for testing purpose, Function call will be from main file
def add_item_in_db_for_testing_api():
    for item in sample_data["external-recruitment-service"]:
        skill = MutableList(sorted(item["skillsets"]))
        current_item = ersTBL(
            candidateId=item["candidateId"],
            fullname=item["fullname"],
            skillsets=skill,
        )
        if not ersTBL.query.filter_by(candidateId=item["candidateId"]).all():
            db.session.add(current_item)
            db.session.commit()

    for item in sample_data["internal-recruitment-service"]:
        skill = MutableList(sorted(item["skillsets"]))
        current_item = irsTBL(
            candidateId=item["candidateId"],
            fullname=item["fullname"],
            skillsets=skill,
        )
        if not irsTBL.query.filter_by(candidateId=item["candidateId"]).all():
            db.session.add(current_item)
            db.session.commit()


# This Function will use in Resource class for Awaring user to avoid duplicate of CandidateId


def get_last_added_candidateId(table_name):
    item = table_name.query.order_by(table_name.candidateId.desc()).first()
    return item.candidateId


# This Function Will Match in Table with given skillset and USE in Both IRS AND ERS Resources class


def check_tbl_with_Givenskillsets(tbl_name, req_skill):
    m = []
    candidates = tbl_name.query.filter_by(skillsets=req_skill, status=True).all()
    for candidate in candidates:
        m.append(
            {
                "candidateId": candidate.candidateId,
                "fullname": candidate.fullname,
                "skillsets": candidate.skillsets,
            }
        )
    return m


# Resource Class For API


class ersFirst(Resource):
    method_decorators = [my_logger]

    def get(self):
        try:
            if not request.args:
                data = request.get_json()
                required_data = data["required_skillsets"]
            else:
                args = request.args
                required_data = args["required_skillsets"]
                required_data = required_data.split(",")
                if len(required_data) == 0:
                    raise Exception

        except Exception:
            return {
                "msg": "Aww! You Can send data via query parameter or via json file by given format Only!",
                "format_query_parameter": "required_skillsets should be separated by comma(,) EXAMPLE: required_skillsets=java,python,sql",
                "format_json": "list_of_string_of_required_skillsets EXAMPLE: required_skillsets:[skill1,skill2,..,skillN] ",
            }
        n = len(required_data)
        req_skill = sorted(required_data)

        candidates = ersTBL.query.filter_by(status=True).all()

        ans = []
        for candidate in candidates:
            skill = list(candidate.skillsets)
            m = len(set(req_skill) & set(skill))
            if m != 0:
                percent = round((m * 100) / n)
                ans.append(
                    {
                        "candidateId": candidate.candidateId,
                        "fullname": candidate.fullname,
                        "skillsets": candidate.skillsets,
                        "percentage_skillsets_match": f"{percent}%",
                    }
                )
        if ans:
            ans = sorted(
                ans,
                key=lambda m: int(m["percentage_skillsets_match"][:-1]),
                reverse=True,
            )
            ans.append({"total_candidate_found": len(ans)})
            return ans
        return (
            {
                "msg": "ooops! No Result Found! Try With Another Skillsets with Given Format Only!",
                "format_query_parameter": "required_skillsets should be separated by comma(,) EXAMPLE: required_skillsets=java,python,sql",
                "format_json": "list_of_string_of_required_skillsets EXAMPLE: required_skillsets:[skill1,skill2,..,skillN] ",
            },
            404,
        )

    def post(self):
        try:
            data = request.get_json()
            cnd_id = data["candidateId"]
            name = data["fullname"]
            if not isinstance(data["skillsets"], list):
                raise Exception()
            skill = MutableList(sorted(data["skillsets"]))

        except Exception:
            return {
                "msg": "Aww! You Can send data via  JSON in HTTP msg body.CandidateId should Be Unique In This Case!",
                "format_json": "candidateId : integer_value, fullname : string_value, skillsets: list_of_string",
            }, 404
        if (
            not ersTBL.query.filter_by(candidateId=cnd_id).first()
            and not irsTBL.query.filter_by(candidateId=cnd_id).first()
        ):
            current_item = ersTBL(
                candidateId=cnd_id,
                fullname=name,
                skillsets=skill,
            )
            db.session.add(current_item)
            db.session.commit()
            return {"msg": f"Data of {name} added successfully for future reference!"}
        if (
            ersTBL.query.filter_by(candidateId=cnd_id).first()
            and not ersTBL.query.filter_by(candidateId=cnd_id).first().status
        ):
            return {
                "msg": "Error! Candidate with Given CandidateId Remove Already, Can't Be Added Again!",
            }, 404
        return {
            "msg": "Error! CandidateId should Be Unique!",
            "last_added_CandidateId": max(
                get_last_added_candidateId(ersTBL), get_last_added_candidateId(irsTBL)
            ),
        }, 404

    def put(self):
        try:
            data = request.get_json()
            cnd_id = data["candidateId"]

        except Exception:
            return {
                "msg": "Aww! You Can send data via  JSON in HTTP msg body.Providing candidateId is Mandatory & Can't Be Updated!",
                "format_json": "candidateId : integer_value, fullname : string_value, skillsets: list_of_string",
            }, 404

        if ersTBL.query.filter_by(candidateId=cnd_id).first():
            current_item = ersTBL.query.filter_by(candidateId=cnd_id).first()
            check = True
            try:
                if data.get("fullname") and current_item.status:
                    name = data.get("fullname")
                    if not isinstance(name, str):
                        raise Exception()
                    current_item.fullname = name
                    db.session.commit()
                    check = False

                if data.get("skillsets") and current_item.status:
                    update_skill = data.get("skillsets")
                    if not isinstance(update_skill, list):
                        raise Exception()
                    existing_skill = list(current_item.skillsets)
                    for item in update_skill:
                        if item not in existing_skill:
                            existing_skill.append(item)
                    existing_skill.sort()
                    current_item.skillsets = MutableList(existing_skill)
                    db.session.commit()
                    check = False

                if data.get("status") and Admin_authentication(
                    request.authorization.username, request.authorization.password
                ):
                    current_item.status = True
                    db.session.commit()
                    check = False
                if not check:
                    return {"msg": "Data Updated Sucessfully!"}
                return {
                    "msg": "you did not provide any data for update or candidate remove already",
                    "NOTE": "For bring back any remove candidate, application need Admin credential as HTTP basic Authorisation",
                    "extra-msg": "Providing candidateId is Mandatory for update operation & For remove profile status=true in JSON",
                    "format_json": "candidateId : integer_value, fullname : string_value, skillsets: list_of_string",
                }, 404

            except Exception:
                return {
                    "msg": "Aww! You Can send data via  JSON in HTTP msg body.Providing candidateId is Mandatory & Can't Be Updated!",
                    "NOTE": "For bring back any remove candidate, application need Admin credential as HTTP basic Authorisation",
                    "extra-msg": "Providing candidateId is Mandatory for update operation & For remove profile status=true in JSON",
                    "format_json": "candidateId : integer_value, fullname : string_value, skillsets: list_of_string",
                }, 404
        return {
            "msg": "Candidate Not Found!Please Try With Another candidateId",
            "format_json": "candidateId : integer_value, fullname : string_value, skillsets: list_of_string",
        }

    def delete(self):
        try:
            if not request.args:
                data = request.get_json()
                required_data = data["cnd_Id"]
            else:
                args = request.args
                required_data = args["cnd_Id"]
                required_data = int(required_data)
        except Exception:
            return {
                "msg": "Aww! You Can send data via query parameter or via json file by given format Only!",
                "format_query_parameter": "For URL query parameter cnd_Id must_be_an_integer_value Example: cnd_Id=5",
                "format_json": "For json data Example: { cnd_Id : must_be_an_integer_value }",
            }
        if ersTBL.query.filter_by(candidateId=required_data, status=True).first():
            current_item = ersTBL.query.filter_by(candidateId=required_data).first()
            current_item.status = False
            db.session.commit()
            return {"msg": "Data Deleted Sucessfully!"}

        return {
            "msg": "Candidate Not Found!Please Try With Another candidateId",
            "format_query_parameter": "For URL query parameter cnd_Id must_be_an_integer_value Example: cnd_Id=5",
            "format_json": "For json data Example: { cnd_Id : must_be_an_integer_value }",
        }


class ersSecond(Resource):
    method_decorators = [my_logger]

    def post(self):
        m = []
        try:
            data = request.get_json()
            required_data = data["requiredSkillsets"]
            if not isinstance(required_data, list):
                raise Exception()
        except Exception:
            return {
                "msg": "Aww! You Can send data via json file by given format Only!",
                "format_json": "requirementId : integer_value, position : string_value, requiredSkillsets: list_of_string",
            }, 404

        req_skill = MutableList(sorted(required_data))
        m = check_tbl_with_Givenskillsets(ersTBL, req_skill)
        if len(m) != 0:
            m.append({"total_candidate_found": len(m)})
            return m
        return {
            "msg": "No data found, Try with another skillset with proper format",
            "format_json": "requirementId : integer_value, position : string_value, requiredSkillsets: list_of_string",
        }, 404


class irsFirst(Resource):
    method_decorators = [user_auth.login_required]

    def post(self):
        try:
            data = request.get_json()
            cnd_id = data["candidateId"]
            name = data["fullname"]
            if not isinstance(data["skillsets"], list):
                raise Exception()
            skill = MutableList(sorted(data["skillsets"]))

        except Exception:
            return {
                "msg": "Aww! You Can send data via  JSON in HTTP msg body.CandidateId should Be Unique In This Case!",
                "format_json": "candidateId : integer_value, fullname : string_value, skillsets: list_of_string",
            }, 404
        if (
            not irsTBL.query.filter_by(candidateId=cnd_id).first()
            and not ersTBL.query.filter_by(candidateId=cnd_id).first()
        ):
            current_item = irsTBL(
                candidateId=cnd_id,
                fullname=name,
                skillsets=skill,
            )
            db.session.add(current_item)
            db.session.commit()
            return {"msg": f"Data of {name} added successfully for future reference!"}
        if (
            irsTBL.query.filter_by(candidateId=cnd_id).first()
            and not irsTBL.query.filter_by(candidateId=cnd_id).first().status
        ):
            return {
                "msg": "Error! Candidate with Given CandidateId Remove Already, Can't Be Added Again!",
            }, 404
        return {
            "msg": "Error! CandidateId should Be Unique!",
            "last_added_CandidateId": max(
                get_last_added_candidateId(ersTBL), get_last_added_candidateId(irsTBL)
            ),
        }, 404


class irsSecond(Resource):
    method_decorators = [user_auth.login_required]

    def post(self):
        m = []
        try:
            data = request.get_json()
            required_data = data["requiredSkillsets"]
            optional_data = data["optionalSkillsets"]
            if not isinstance(required_data, list) and not isinstance(
                optional_data, list
            ):
                raise Exception()
            total_data = required_data + optional_data
        except Exception:
            return {
                "msg": "Aww! You Can send data via json file by given format Only!",
                "format_json": "requirementId : integer_value, position : string_value, requiredSkillsets: list_of_string,optionalSkillsets: list_of_string",
            }, 404

        req_skill = MutableList(sorted(required_data))
        opt_skill = MutableList(sorted(optional_data))
        total_skil = MutableList(sorted(total_data))

        m = check_tbl_with_Givenskillsets(irsTBL, total_skil)
        if len(m) == 0:
            m = check_tbl_with_Givenskillsets(irsTBL, req_skill)
        if len(m) == 0:
            m = check_tbl_with_Givenskillsets(ersTBL, total_skil)
        if len(m) != 0:
            m.append({"total_candidate_found": len(m)})
            return m
        return {
            "msg": "No data found, Try with another skillset with proper format",
            "format_json": "requirementId : integer_value, position : string_value, requiredSkillsets: list_of_string,optionalSkillsets: list_of_string",
        }, 404
