from app import language, config
from app.libs.mysqllib import MysqlLib


class Customers(object):
    """docstring for UserFunctions"""

    def __init__(self, user):
        super(Customers, self).__init__()
        self.dbconn = MysqlLib()
        self.user = user

    def getCustomers(self):
        allCustomers = self.dbconn.select_from_table("customers", condition="ORDER BY id desc")
        return allCustomers
