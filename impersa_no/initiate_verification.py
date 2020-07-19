from django.http import HttpResponse
import json
import mysql.connector
import hashlib
import uuid
import time

def initiate_verification(request):
    verify_employee_webhook = request.POST.get("verify_employee_webhook",None)
    employee_id = request.POST.get("employee_id",None)
    buisness_id = request.POST.get("buisness_id",None)
    print(verify_employee_webhook)
    print(employee_id)
    print(buisness_id)
    if verify_employee_webhook and employee_id and buisness_id:
        customer_link = "cus-link"
        employee_link = "emp-link"
        verifier_link = "ver-link"
        
        dbcreds = open("dbcredentials.txt").read().split("\n")
        my_database = mysql.connector.connect(
          host=dbcreds[0],
          user=dbcreds[1],
          password=dbcreds[2],
          auth_plugin='mysql_native_password'
        )
        
        mycursor = my_database.cursor()
        mycursor.execute(
            "INSERT INTO impersa_no.verifications "+
            "(buisness_id,employee_id,customer_link,employee_link,"+
            "customer_allowed,employee_clip,verifier_allowed,verifier_link,verifier_ready)"+
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (int(buisness_id),int(employee_id),customer_link,employee_link,
             None,None,None,verifier_link,verify_employee_webhook)
        )
        my_database.commit()
        
        response = json.dumps({
            "customer":customer_link,
            "employee":employee_link
            })
        return HttpResponse(response)
    else:
        return HttpResponse("error",status=400)
