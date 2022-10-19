from .models import Lot
from core.product.models import Product
# Lot

def calculate_stock(stock, quantity_in):
    current = int(stock)
    quantity_in = int(quantity_in)
    data = {}
    try:
        stock = current + quantity_in
        return stock
    except Exception as e:
        data['error'] = str(e)


# Get total:
def get_total(price, quantity, product_id):
    price = float(price)
    quantity = float(quantity)
    product_id = product_id
    try:
        product = Product.objects.get(pk=product_id)
        iva = product.get_iva()
        sub_total = price * quantity
        total = round(((sub_total/100) * iva), 2)
        return total
    except Exception as e:
        print(str(e))


# Boolean returns ON and OF and I need to returns True or False
def is_boolean(condition):
    if condition == 'on':
        return True
    else:
        return False
