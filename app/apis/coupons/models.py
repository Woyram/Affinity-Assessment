from app import language, config
from app.libs.mysqllib import MysqlLib


class Coupons(object):
    """docstring for UserFunctions"""

    def __init__(self, user):
        super(Coupons, self).__init__()
        self.dbconn = MysqlLib()
        self.user = user

    def getUploads(self):
        allUploads = self.dbconn.select_from_table("uploads", condition="ORDER BY id desc")
        return allUploads

    def add_customer(self, request_data):
        print("In Here to Add the Customer")

        customer = self.dbconn.insert_in_table("customers", request_data)
        return customer

    def get_coupons(self, upload_id):
        coupons = self.dbconn.joint_select("coupons", ["customers"], ["coupons.*", "customers.customer_name"],
                                           ["coupons.customer_id=customers.customer_id"],
                                           gen_condition="where coupons.upload_id = '{}'".format(upload_id))
        return coupons

    def get_customer(self, customer_id):

        condition = "customer_id = '{}'".format(customer_id)
        customer = self.dbconn.find_one("customers", condition=condition)
        return customer

    def add_coupon(self, coupon_data):
        print("In Here to add Coupon")

        coupon = self.dbconn.insert_in_table("coupons", coupon_data)
        return coupon

    def add_upload_data(self, upload_data):
        print("In Here to add Upload Data")

        upload = self.dbconn.insert_in_table_ret_id("uploads", upload_data)
        return upload
