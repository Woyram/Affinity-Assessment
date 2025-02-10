import pytest
import datetime
from unittest.mock import patch, MagicMock
from io import StringIO

from app.apis.coupons.services import CouponsServices


@pytest.fixture
def mock_coupon_service():
    """Fixture to mock the coupon service with database connection."""
    mock_service = MagicMock()
    mock_service.model = MagicMock()

    # Mock the methods that will be used
    mock_service.generate_coupons = CouponsServices({})
    mock_service.read_csv = CouponsServices({})
    mock_service.process_file = CouponsServices({})
    mock_service.get_customer = MagicMock()
    mock_service.add_coupon = MagicMock()
    mock_service.add_upload_data = MagicMock()

    return mock_service


@patch("os.makedirs")  # Mock directory creation
@patch("os.path.exists", return_value=False)  # Mock directory existence check
def test_generate_coupons_valid_file(mock_exists, mock_makedirs, mock_coupon_service):
    """Test that the generate_coupons function processes a valid CSV file correctly."""

    mock_coupon_service.read_csv.return_value = (["customer_id", "customer_name"], [["AFF0143", "Osei"]])
    mock_coupon_service.process_file.return_value = True  # Ensure process_file returns True

    session_data = {"username": "admin"}
    csv_file = MagicMock()
    csv_file.filename = "test.csv"

    # Call generate_coupons
    result = mock_coupon_service.generate_coupons(session_data, csv_file)

    # Mocking the expected return value
    mock_coupon_service.generate_coupons.return_value = {
        "code": "SUCCESS",
        "msg": "Coupons Generated Successfully.",
        "data": []
    }

    assert result["code"] == "SUCCESS"
    assert result["msg"] == "Coupons Generated Successfully."

@patch("builtins.open", new_callable=lambda: StringIO("customer_id,customer_name\nAFF0143,Osei\n"))
def test_process_file_assigns_correct_coupon(mock_open, mock_coupon_service):
    """Test that process_file assigns correct voucher based on order value."""

    mock_coupon_service.model.get_customer.return_value = {"order_value": 6000}

    # Call process_file
    mock_coupon_service.process_file(["customer_id", "customer_name"], [["AFF0143", "Osei"]],
                                     {"username": "admin"}, "test.csv", "UPLOAD123")

    # Ensure add_coupon was called
    mock_coupon_service.model.add_coupon.assert_called_once()

    # Get the arguments passed to add_coupon
    args, _ = mock_coupon_service.model.add_coupon.call_args
    assert args[0]["voucher_amount"] == 500  # Order value 6000 should get a 500 voucher

def test_get_customer(mock_coupon_service):
    """Test retrieving a customer."""

    mock_coupon_service.model.get_customer.return_value = {"customer_id": "AFF0143", "order_value": 5000}

    # Call get_customer
    result = mock_coupon_service.model.get_customer("AFF0143")

    assert result["order_value"] == 5000
    mock_coupon_service.model.get_customer.assert_called_once_with("AFF0143")


def test_add_coupon(mock_coupon_service):
    """Test adding a coupon to the database."""

    coupon_data = {"coupon_id": "12345", "customer_id": "AFF0143", "voucher_amount": 100}

    # Call add_coupon
    mock_coupon_service.model.add_coupon(coupon_data)

    # Ensure the insert_in_table method is called
    mock_coupon_service.model.insert_in_table.assert_called_once_with("coupons", coupon_data)


def test_add_upload_data(mock_coupon_service):
    """Test adding upload data."""

    upload_data = {"upload_date": datetime.datetime.now(), "upload_id": "UPLOAD123", "file_name": "test.csv"}

    # Call add_upload_data
    mock_coupon_service.model.add_upload_data(upload_data)

    # Ensure insert_in_table_ret_id is called
    mock_coupon_service.model.insert_in_table_ret_id.assert_called_once_with("uploads", upload_data)
