import csv
import os
import traceback
import random
import time
from datetime import datetime

from app import config
from app import language
from app.apis.coupons.models import Coupons
from app.libs.logger import Logger


class CouponsServices(object):
    """
    Class contains functions and attributes for authtentication
    Function: * getCampainge(sel)
    """

    def __init__(self, user):
        self.lang = {}
        self.lang = getattr(language, config.DEFAULT_LANG)
        self.user = user
        self.model = Coupons(user)
        self.logger = Logger()

    def getUploads(self):
        print("In Here to get all uploads")

        uploads = self.model.getUploads()
        return uploads

    def get_upload_coupons(self, upload_id):
        print("In Here to get coupons for Upload - {}".format(upload_id))

        coupons = self.model.get_coupons(upload_id)
        return coupons

    def generate_coupons(self, session_data, csv_file):
        print("Here to generate the coupons for these users.")
        try:
            print("We got here...")
            if csv_file.filename == "":
                return {"code": language.CODES['FAIL'], "msg": language.en['no_file_to_upload'],
                        "data": []}
            processFile = False

            if csv_file and csv_file.filename.rsplit('.', 1)[1].lower() not in ["csv", "xls"]:
                return {"code": "FAIL", "msg": "No file uploaded", "data": []}

            print("File is a csv")
            file_path = config.UPLOAD_FOLDER
            print(file_path)

            os.makedirs(file_path, exist_ok=True)
            filename, file_extension = os.path.splitext(csv_file.filename)

            new_filename = csv_file.filename
            counter = 1
            while os.path.exists(os.path.join(file_path, new_filename)):
                new_filename = f"{filename}_{int(time.time())}_{counter}{file_extension}"
                counter += 1

            save_path = os.path.join(file_path, new_filename)
            print("SAVE PATH - {}".format(save_path))
            user_csv = csv_file.save(save_path)
            print(user_csv)

            # Read fields and data from the CSV file
            fields, data = self.read_csv(save_path)
            generated_id = f"AFF{str(datetime.now())}"
            upload_id = generated_id.replace(' ', '').replace('-', '').replace(':', '').replace('.', '')

            print("FILE NAME --- {}".format(new_filename))
            processFile = self.process_file(fields, data, session_data, new_filename, upload_id)

            print(csv_file)
            if processFile:
                return {"code": language.CODES['SUCCESS'], "msg": "Coupons Generated Successfully.", "data": []}

        except Exception as expt:
            traceback.print_exc()
            return {'code': language.CODES['ERROR'], 'msg': 'Customers failed. Error({})'.format(str(expt))}

    def read_csv(self, file_path):
        fields = []
        data = []

        with open(file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)  # Get the header/field names
            data = [row for row in csvreader]  # Get data rows

        return fields, data

    def process_file(self, fields, data, session_data, file_name, upload_id):
        print("In Saving the data in the files")
        print(data)

        coupon_rules = [
            {"min": 1000, "max": 5000, "voucher": 100, "validity": 1},
            {"min": 5000, "max": 10000, "voucher": 500, "validity": 5},
            {"min": 10000, "max": float('inf'), "voucher": 1000, "validity": 10},
        ]

        for row in data:
            try:
                customer_id = row[0]
                customer_name = row[1]

                get_customer = self.model.get_customer(customer_id)
                print(get_customer)

                if get_customer:
                    print(customer_name)

                    # Assign coupon based on order value
                    assigned_coupon = next((c for c in coupon_rules if c["min"] <= float(get_customer["order_value"]) < c["max"]), None)
                    print("__________________________")
                    print(assigned_coupon)
                    print("__________________________")

                    if assigned_coupon:
                        coupon_id = str(random.randint(10000, 99999))
                        coupon_data = {
                            "coupon_id": coupon_id,
                            "customer_id": customer_id,
                            "upload_id": upload_id,
                            "voucher_amount": assigned_coupon["voucher"],
                            "validity_days": assigned_coupon["validity"],
                            "status": 1
                        }
                        self.model.add_coupon(coupon_data)

                        print(f"Generated Coupon: {coupon_data}")

            except Exception as e:
                print(f"Error processing row {row}: {e}")
                continue

        # Add Upload data...
        upload_data = {
            "upload_date": datetime.now(),
            "upload_id": upload_id,
            "uploaded_by": session_data["username"],
            "file_name": file_name,
            "status": 1
        }
        self.model.add_upload_data(upload_data)
        return True
