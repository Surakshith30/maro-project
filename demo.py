
add_to_cart = {1:3, #product_id : product_quantity
        2:5}
cart_details={'total_amt':'',
              'products':}
temp_list = []
for key in add_to_cart.keys():
    temp = {'id':r.id,'product_name':r.product_name,'product_cost':r.product_cost,
            'product_quantity':r.product_quantity,}
    temp_list.append(temp)

