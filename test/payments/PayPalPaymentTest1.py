from payments.paypal import ExecutePayPalOrder

execute = ExecutePayPalOrder()
response1 = execute.CreateProduct()
print(response1)