import datetime

def get_product_info():
    """
      Reads product master CSV and returns a dictionary of product_id to product_price.

      Returns:
          dict: product_id as key and price as value
      """
    product_info = {}
    with open(r'..\product_master\product_master.csv') as pm:
        products = pm.readlines()[1:]
        for product in products:
            product_info[product.split(',')[0]] = product.split(',')[2]
        return product_info

def validate_sales(order, product_info):
    """ Validates that the sales amount is equal to price * quantity. """
    try:
        if order['product_id'] in product_info:
            price = int(product_info[order['product_id']])
            quantity = int(order['quantity'])
            sales = int(order['sales'])
            return price * quantity == sales
    except (ValueError, TypeError, KeyError):
        return False
    return False

def validate_id(id_, product):
    """ Checks whether the product ID exists in the product master list."""
    if id_ in product:
        return True
    return False

def validate_order_date(date):
    """ Validates that the order date is not a future date."""
    dt = datetime.datetime.strptime(date, '%d-%m-%Y').date()
    today_date = datetime.date.today()
    day = (today_date - dt).days
    if day >= 0:
        return True
    return False

def validate_city(city):
    """ Checks if the city is one of the allowed delivery cities."""
    if city in ['Mumbai','Bengaluru','Delhi']:
        return True
    return False

def validate_empty(orders):
    """ Checks for empty fields in the order."""
    empty_col = []
    for k, v in orders.items():
        if not orders[k] or orders[k] == '':
            empty_col.append(k)
    return empty_col

def read_master_data():
    """ Reads the product master CSV file and returns a list of valid product IDs."""
    product_list = []
    with open(r'..\product_master\product_master.csv') as pm:
        products = pm.readlines()[1:]
        for product in products:
            product_list.append(product.split(',')[0])
        return product_list
