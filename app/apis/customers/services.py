from app import config
from app import language
from app.apis.customers.models import Customers
from app.libs.logger import Logger


class customerServices(object):
    """
    Class contains functions and attributes for authtentication
    Function: * getCampainge(sel)
    """

    def __init__(self, user):
        self.lang = {}
        self.lang = getattr(language, config.DEFAULT_LANG)
        self.user = user
        self.model = Customers(user)
        self.logger = Logger()

    def get_customers(self):
        print("In Here to get all customers")

        customers = self.model.getCustomers()
        return customers
