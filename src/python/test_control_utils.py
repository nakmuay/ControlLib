import control_utils as utils

na = range(3)
nb = range(10, 13)

for order in utils.arx_orders(na, nb):
    print(order)
