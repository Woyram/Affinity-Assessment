"""
English language translation
"""

en = {
    "login_successful": "Login Successful",
    "none_found": "None Found",
    "data_found": "Data Found",
    "emails_exist": "Email Exist",
    "mobile_exist": "Mobile Number Exist",
    "mobile_empty": "Mobile Number Field Empty",
    "user_add_failed": "User Addition Failed",
    "user_added": "User Added Successfully",
    "user_not_added": "User Not Added",
    "wrong_username": "Wrong Username",
    "wrong_password": "Wrong Password",
    "image_size_big": "Image Too Big",
    "file_not_uploaded": "File Not Uploaded",
    "invalid_login": "Invalid Login",
    "has_pending_loan": "User Has Pending Loan",
    "no_loan_found": "No Loan Found.",
    "has_loan": "User Has A Loan",
    "has_requested_loan": "User Has A Requested Loan",
    "exceeds_threshold": "Loan Exceeds Threshold",
    "loan_requested": "Loan Requested Successfully",
    "loan_updated": "Loan Updated Successfully.",
    "loan_failed": "Loan Request Failed",
    "user_not_found": "User Not Found",
    "not_enough_funds": "Not Enough Funds For Transaction",
    "withdrawal_successful": "Withdrawal Successful",
    "deposit_successful": "Deposit Successful",
    "loan_not_found": "Loan Found",
    "sms_successful": "SMS Send Successfully",
    "sms_failed": "SMS Send Failed",
    "loan_not_exist": "User Has No Loan",
    "user_deactivation_failed": "User Deactivation Failed",
    "user_deactivation_successful": "User Deactivation Successful",
    "loan_denied_successful": "Loan {} Successfully",
    "loan_approval_successful": "Loan {} Successfully",
    "loan_approval_failed": "Loan Approval Failed",
    "withdrawal_message": "You have successfully made a withdrawal of GHC{}. Your current balance is GHC{}.",
    "deposit_message": "You have successfully made a deposit of GHC{}. Your current balance is GHC{}.",
    "loan_payment": "You have successfully made a payment of GHC{} of your loan. Your loan balance is GHC{}.",
    "loan_request": "Hello {} {}, you have requested a loan of GHC{}. You will be notified when your loan is "
                    "approved. Thank You.",
    "account_creation": "Your Account Has Been Created Successfully. Your account number is: {}.",
    "loan_approval": "Hello {} {}. Your loan of GHC{} has been {}. You are to pay an amount of GHC{} {}. "
                     "Thank you.",
    "loan_completed": "Congratulations, you have completed the payment of your loan. You can request another loan "
                      "after 2 months. Thank You.",
    "transaction_not_found": "Transaction Not Found",
    "transaction_found": "Transaction Found",
    "user_updated_successfully": "User Updated Successfully",
    "user_update_failed": "User Update Failed",
    "delete_system_user_failed": "Delete System User Failed",
    "signed_docs_successful": "Signed Documents Uploaded Successfully",
    "signed_docs_failed": "Signed Documents Upload Failed",
    "delete_system_user_successful": "Delete System User Successful",
    "images_must_be_provided": "Images Must Be Provided",
    "15_days_loan_notice": "Hello {} {}, you have 15 days left to pay off your requested loan, {}. "
                           "Kindly make payment to keep your chances of requesting another.",
    "today_loan_notice": "Hello {} {}, your requested loan, {} is due today. Kindly make payment to keep "
                           "your chances of requesting another.",
    "send_new_user_sms_password": "Hello {}, your account has been created successfully. Your username is {} and your "
                                  "password is {}. Please change your password when you log in.",
    "error_sending_code": "Error sending OTP.",
    "password_mismatch": "Passwords do not match.",
    "password_not_set": "Failed to set password.",
    "password_set": "Password Set Successfully.",
    "failed_add_branch": "Failed to add Branch.",
    "branch_added_successfully": "Branch Added Successfully.",
}

"""
Application response codes
"""
CODES = {
    "FAIL": "01",
    "SUCCESS": "00",
    "ERROR": "02",
}


"""
Menu Styles
"""
STYLE = {
    "home_style": {"home": "color:#F68500"},
    "bulkpay_style": {"bulkpay": "color:#F68500"},
    "dashboard_style": {"dashboard": "color:#F68500"},
    "trans_style": {"transactions": "color:#F68500"},
    "admins_style": {"admins": "color:#F68500"},
    "inst_style": {"inst": "color:#F68500"},
    "mer_style": {"mer": "color:#F68500"},
    "auto_style": {"auto": "color:#F68500"},
    "logs_style": {"logs": "color:#F68500"},
    "settings_style": {"settings": "color:#F68500"},
    "prod": {"products": "color:#F68500"},
    "account_style": {"account": "color:#F68500"},
    "tup_style": {"topups": "color:#F68500"},
}