from payments.paypal import ExecutePayPalOrder

execute = ExecutePayPalOrder()
response1 = execute.CreateSubscription()
print(response1)