import datetime
import random
from datetime import datetime

from app import config

from passlib.hash import sha256_crypt
from app import language
from flask import request

from app.apis.admins.models import Administrator
from app.libs.logger import Logger
from app.libs.sms import SMS


class adminServices(object):
    """
    Class contains functions and attributes for authentication
    Function: * getCampaign(sel)
    """

    def __init__(self, user):
        self.SMS = SMS()
        self.lang = {}
        self.lang = getattr(language, config.DEFAULT_LANG)
        self.user = user
        self.model = Administrator(user)
        self.logger = Logger()

    def adminLogin(self, request_data, try_var):
        """
        This function handles all logic related to log in on the platform
        @Params : void
        """
        self.logger.write_to_console("EVENT", "Login request for " + request_data['username'])

        admin_data = self.model.get_admin_by_username_login(request_data['username'])

        if admin_data == []:
            print("I came hereeeeeee")
            self.logger.write_log("USER_ACCESS",
                                  "Login request | " + request_data['username'] + " | Failed | Non-Existing User.")
            return {"code": language.CODES['FAIL'], "msg": language.en['invalid_login'], "data": []}
        else:
            print(try_var)
            if try_var != None and try_var >= 3:
                self.model.update_administrator(
                    {"status": "1", "last_login": "NOW()", "username": request_data['username']})
                if try_var == 3:
                    return {"code": language.CODES['FAIL'],
                            "msg": "Sorry your account has been blocked. Kindly contact your administrator.",
                            "data": [],
                            "username": request_data['username']}
                else:
                    return {"code": language.CODES['FAIL'],
                            "msg": "Sorry your account has been blocked. Kindly contact your administrator.",
                            "data": []}

            else:
                if admin_data[0]['user_status'] == 1:
                    print(admin_data[0])
                    verify_pass = sha256_crypt.verify(request_data['password'], admin_data[0]['password'])
                    self.logger.write_to_console("EVENT", "verify Password | " + str(verify_pass))

                    if verify_pass:
                        self.model.update_administrator(
                            {"status": "1", "last_login": "NOW()", "username": request_data['username']})
                        self.logger.write_log("USER_ACCESS", "Login request | " + request_data[
                            'username'] + " | Successful | Login Successful")
                        return {"code": language.CODES['SUCCESS'], "msg": self.lang['login_successful'],
                                "data": admin_data[0], "username": request_data['username']}
                    else:
                        self.logger.write_to_console("EVENT", "Login request failed for " + request_data[
                            'username'] + " | Failed | Wrong Password.")
                        return {"code": language.CODES['FAIL'], "msg": self.lang['invalid_login'], "data": 1,
                                "username": request_data['username']}

                else:
                    self.logger.write_to_console("EVENT", "Login request failed for " + request_data[
                        'username'] + " | Failed | Blocked User")
                    return {"code": language.CODES['FAIL'],
                            "msg": "Sorry your account has been blocked. Kindly contact your administrator.", "data": 2,
                            "username": request_data['username']}

    def adminLogout(self):
        result = self.model.update_administrator({"status": "0", "username": self.user['username']})
        return result

    def sendResetCode(self, request_data):
        print("Hello")

        mobile_number = request_data["userMobile"]
        print("Request Number")
        print(mobile_number)

        getUserDetails = self.model.getUser(self.SMS.validateNumber(mobile_number))
        print("-------------------")
        print(getUserDetails)
        if getUserDetails == []:
            print("No user found.")
        else:
            # Take the users phone and send the sms and then add the users table.
            print("...Call them...")
            code = random.randint(1000, 9999)
            sendSMS = self.SMS.sendPillowSMS(self.SMS.validateNumber(mobile_number).strip(),
                                             "Your OTP is {}".format(code))
            print(sendSMS)

            # Now, let's add it to the admin_login table.
            update_data = {
                "reset_code": code
            }

            addResetCode = self.model.update_user_reset(update_data, getUserDetails["user_id"])
            print(addResetCode)

            if addResetCode:
                return {"code": language.CODES['SUCCESS'], "msg": self.lang['delete_system_user_successful'],
                        "data": {}}
            else:
                return {"code": language.CODES['FAIL'], "msg": self.lang['error_sending_code'],
                        "data": []}

    def setUserPassword(self, request_data):
        print("In Set User Password")
        print(request_data)

        password = request_data["password"]
        confirm_password = request_data["userPassword"]
        otp_code = request_data["code"]

        # Check if both passwords are the same.
        if password != confirm_password:
            return {"code": language.CODES['FAIL'], "msg": self.lang['password_mismatch'],
                    "data": []}

        # Let us go and select the user and the get the details.
        getUser = self.model.getUserByOTPCode(otp_code)
        print("ooooooOOoooooooooooo")
        print(getUser)
        if getUser == []:
            return {"code": language.CODES['FAIL'], "msg": self.lang['user_not_found'],
                    "data": []}
        else:
            # Set the password now.
            createPass = sha256_crypt.hash(password)
            update_data = {
                "password": createPass
            }

            update_user_reset_code_data = {
                "reset_code": ""
            }

            setPassword = self.model.updateUserPassword(update_data, getUser["user_id"])
            setCode = self.model.updateUserCode(update_user_reset_code_data, getUser["user_id"])
            if setPassword and setCode:
                return {"code": language.CODES['SUCCESS'], "msg": self.lang['password_set'],
                        "data": {}}
            else:
                return {"code": language.CODES['FAIL'], "msg": self.lang['password_not_set'],
                        "data": []}

    def pagination(self, request_list):
        print("Here to Paginate the table")

        page = int(request.args.get('page', 1))
        per_page = 15
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page

        items = request_list[start_idx:end_idx]
        total_pages = len(request_list) // per_page + (len(request_list) % per_page > 0)

        return {"current_page": page, "total_pages": total_pages, "item": items}

    def getAllAdministrators(self, request_data):
        """
            This function handles all logic related to log in on the platform

            @Params : void
        """

        if request_data == {}:
            request_data = {'offset': 0, 'records': 11, 'fromdate': '', 'user_right_id': '', "branch": '', 'active': ''}
        else:
            request_data['offset'] = int(request_data['page']) * 11
            request_data['records'] = 11

        # inst_model = Institution(self.user)

        self.logger.write_to_console("EVENT", "Getting administrator list for {} -> {}".format(self.user['username'],
                                                                                               request_data))

        # if self.user['branch_code'] == "All":
        administrators_data = self.model.get_all_administrators(request_data)
        admin_groups_data = self.model.get_admin_groups()
        branches_data = []
        # else:
        #     administrators_data = self.model.get_all_administrators_by_branch(request_data)
        #     admin_groups_data =  self.model.get_admin_groups()
        #     branches_data =  self.model.get_branches({'page': 0, 'offset': 0, 'records': 1000})

        for result in administrators_data:
            print(result)
            if "created" in result and result["created"] is not None:
                result["created"] = result["created"].strftime("%Y-%m-%d %H:%M:%S")
            if "last_login" in result and result["last_login"] is not None:
                result["last_login"] = result["last_login"].strftime("%Y-%m-%d %H:%M:%S")

            if "pass_date" in result and result["pass_date"] is not None:
                result["pass_date"] = result["pass_date"].strftime("%Y-%m-%d %H:%M:%S")

        self.logger.write_to_console("EVENT",
                                     "Administrators list gotten successfully for {}".format(self.user['username']))
        return {"code": language.CODES['SUCCESS'], "msg": self.lang['data_retrieved'], "data": administrators_data,
                'admin_group': admin_groups_data, 'branches': branches_data}

    def dumpDatabase(self):
        print("Dump Database")

        now = datetime.now()
        formatted_date = now.strftime("%Y%m%d_%H%M%S")
        dumpDatabase = self.model.dumpDatabase(config.DATABASE_FOLDER.format(formatted_date))
        print(f"DUMPED IT: {dumpDatabase}")

        return {"code": "00", "data": "", "msg": "Dump Completed."}
