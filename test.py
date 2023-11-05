from payments.paypal import ExecutePayPalOrder

execute = ExecutePayPalOrder()
response1 = execute.CreatePlan()
print(response1)