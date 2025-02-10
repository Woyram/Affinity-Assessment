from app.libs.mysqllib import MysqlLib


class Dashboard(object):
    """docstring for UserFunctions"""

    def __init__(self, user):
        super(Dashboard, self).__init__()
        self.dbconn = MysqlLib()
        self.user = user

    def getAllMale(self):
        print("In Get All Male")

        condition = "where gender = 'male' and user_type = '105'"
        data = self.dbconn.select_count_table("users", condition=condition)
        return data

    def get_item_count(self, item):
        print("To Get Count for {}".format(item))

        customers = self.dbconn.select_count_table(item)
        return customers

    def getApprovedLoansAmount(self, status):
        print("In Get Approved Loans Amount")

        approvedLoans = self.dbconn.joint_select("loans", ["users"],
                                                 ["SUM(loans.loan_capital) as SUM"],
                                                 ["loans.user_id = users.user_id"],
                                                 gen_condition="WHERE loans.status = '{}'".format(status)
                                                 .format(status))

        return approvedLoans

    def getAllUsers(self):
        print("In Get All Users")

        data = self.dbconn.select_count_table("users", condition="WHERE user_type = '105'")
        return data
