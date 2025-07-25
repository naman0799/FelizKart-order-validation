import pytest
import validator
import datetime
from unittest.mock import patch

# Test validate_id()
def test_validate_id_valid():
    product_list = ['P123', 'P456']
    assert validator.validate_id('P123', product_list)

def test_validate_id_invalid():
    product_list = ['P123', 'P456']
    assert not validator.validate_id('P999', product_list)

# Test validate_order_date()
def test_validate_order_date_valid():
    today = datetime.date.today().strftime('%d-%m-%Y')
    assert validator.validate_order_date(today)

def test_validate_order_date_future():
    future = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%d-%m-%Y')
    assert not validator.validate_order_date(future)

# Test validate_empty()
def test_validate_empty_fields():
    order = {
        'order_id': '1',
        'order_date': '',
        'product_id': 'P123',
        'quantity': '',
        'sales': '200',
        'city': 'Delhi'}

    result = validator.validate_empty(order)
    assert 'order_date' in result
    assert 'quantity' in result

# Test validate_sales() using mock (to avoid reading product_master.csv every time)
@patch('validator.get_product_info')
def test_validate_sales_valid(mock_product_info):
    mock_product_info.return_value = {'P123': '100'}
    order = {'product_id': 'P123', 'quantity': '2', 'sales': '200'}
    assert validator.validate_sales(order, mock_product_info.return_value)

@patch('validator.get_product_info')
def test_validate_sales_invalid(mock_product_info):
    mock_product_info.return_value = {'P123': '100'}
    order = {'product_id': 'P123', 'quantity': '2', 'sales': '250'}
    assert not validator.validate_sales(order, mock_product_info.return_value)
