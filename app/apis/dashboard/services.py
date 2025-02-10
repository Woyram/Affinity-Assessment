from app import config
from app import language
from app.apis.dashboard.models import Dashboard
from app.libs.logger import Logger


class dashboardServices(object):
    """
    Class contains functions and attributes for authtentication
    Function: * getCampainge(sel)
    """

    def __init__(self, user):
        self.lang = {}
        self.lang = getattr(language, config.DEFAULT_LANG)
        self.user = user
        self.model = Dashboard(user)
        self.logger = Logger()

    def get_dashboard_info(self):
        print("Get All Dashboard Info")

        tables = ["customers", "coupons", "uploads"]
        response = {table: self.model.get_item_count(table)[0].get("count", 0) for table in tables}

        print(response)
        return response
