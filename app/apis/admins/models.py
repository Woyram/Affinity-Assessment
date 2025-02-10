from app import config

from app.libs.mysqllib import MysqlLib


class Administrator(object):
    """
    docstring for UserFunctions
    """

    def __init__(self, user):
        super(Administrator, self).__init__()
        self.dbconn = MysqlLib()
        self.user = user

    def get_admin_by_username_login(self, username):
        admin = self.dbconn.joint_select("admin_login", ["user_types", "users"],
                                         ["admin_login.password", "admin_login.username",
                                          "admin_login.user_type",
                                          "users.firstname",
                                          "users.lastname", "users.email",
                                          "admin_login.last_login",
                                          "admin_login.pass_date", "admin_login.status", "users.status as user_status",
                                          "admin_login.date_created",
                                          "user_types.rights_name", "user_types.details"],
                                         ["admin_login.user_type = user_types.rights_id",
                                          "admin_login.user_id = users.user_id"],
                                         gen_condition="WHERE admin_login.username= '" + username + "'")
        return admin

    def getUser(self, mobile_number):
        user = self.dbconn.joint_select('admin_login', ["users"], ["admin_login.username",
                                                                   "admin_login.email", "users.mobile",
                                                                   "users.firstname", "users.user_id"],
                                        ["admin_login.user_id = users.user_id"],
                                        gen_condition="where users.mobile= {}".format(mobile_number))
        return user[0]

    def getUserByOTPCode(self, otp_code):
        user = self.dbconn.select_from_table("admin_login", condition="Where reset_code = {}".format(otp_code))
        return user[0]

    def updateUserPassword(self, data, user_id):
        print("Update User Password")

        updateUser = self.dbconn.update_table("admin_login", data, "WHERE user_id = {}".format(user_id))
        return updateUser

    def updateUserCode(self, data, user_id):
        print("Update User Code")

        updateUser = self.dbconn.update_table("admin_login", data, "WHERE user_id = {}".format(user_id))
        return updateUser

    def update_administrator(self, data):
        admin = self.dbconn.update_table("admin_login", data, "WHERE username='{}'".format(data['username']))
        return admin

    def update_user_reset(self, data, user_id):
        admin = self.dbconn.update_table("admin_login", data, "WHERE user_id = {}".format(user_id))
        return admin

    def get_admin_groups(self):
        data = self.dbconn.select_from_table("tbl_user_right", condition="where rights_id != 123456789")
        return data

    def get_all_administrators(self, request_params):

        where_con_list = []
        where_con = ''

        if 'active' in request_params != "" and request_params['active'] != "" and request_params['active'] != "All":
            where_con_list.append("active='{}' ".format(request_params['active']))

        if 'user_right_id' in request_params != "" and request_params['user_right_id'] != "":
            where_con_list.append("user_right_id='{}' ".format(request_params['user_right_id']))

        if 'branch' in request_params != "" and request_params['branch'] != "" and request_params['branch'] != "All":
            where_con_list.append("branch='{}' ".format(request_params['branch']))

        where_con = " and ".join(where_con_list)
        if where_con == "":
            where_con = "1"

        if request_params['fromdate'] == "" or request_params['todate'] == "":
            data = self.dbconn.joint_select_paged("tbl_login", ["tbl_user_right"],
                                                  ["tbl_login.username", "tbl_login.user_right_id",
                                                   "tbl_login.first_name", "tbl_login.last_name", "tbl_login.email",
                                                   "tbl_login.msisdn", "tbl_login.last_login", "tbl_login.active",
                                                   "tbl_login.status", "tbl_login.created", "tbl_user_right.name",
                                                   "tbl_user_right.details"],
                                                  ["tbl_login.user_right_id=tbl_user_right.rights_id"],
                                                  "WHERE " + where_con + " ORDER BY created DESC",
                                                  offset=request_params['offset'], records=request_params['records'])
        else:
            data = self.dbconn.joint_select_paged("tbl_login", ["tbl_user_right"],
                                                  ["tbl_login.username", "tbl_login.user_right_id",
                                                   "tbl_login.first_name", "tbl_login.last_name", "tbl_login.email",
                                                   "tbl_login.msisdn", "tbl_login.last_login", "tbl_login.active",
                                                   "tbl_login.status", "tbl_login.created", "tbl_user_right.name",
                                                   "tbl_user_right.details"],
                                                  ["tbl_login.user_right_id=tbl_user_right.rights_id"],
                                                  "WHERE " + where_con + " and created between '{0}' and '{1}' ORDER BY created DESC".format(
                                                      request_params['fromdate'], request_params['todate']),
                                                  offset=request_params['offset'], records=request_params['records'])
        return data

    def dumpDatabase(self, database_path):
        print("Database Dump Path")

        dump = self.dbconn.dump_database(config.MYSQL_HOST, config.MYSQL_PASSWD, config.MYSQL_USER,
                                         config.MYSQL_DATABASE, database_path)

        print(dump)
        return True
