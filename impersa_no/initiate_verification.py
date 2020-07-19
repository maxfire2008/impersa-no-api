from django.http import HttpResponse
import json
import mysql.connector
import hashlib
import uuid
import time
import os

WORKING_URL = open("WORKING_URL.txt").read()

DBCREDS = os.environ["IMPERSANODBCREDENTIALS"].split(":")

class ChrSets:
    Hex = "abcdef1234567890"

def parse(x,chrset):
    x=str(x)
    chrset=list(chrset)
    out = ""
    for i in x:
        if i in chrset:
            out+=i
    return out

def initiate_verification(request):
    verify_employee_webhook = request.POST.get("verify_employee_webhook",None)
    employee_id = request.POST.get("employee_id",None)
    buisness_id = request.POST.get("buisness_id",None)
    api_key = parse(request.POST.get("api_key",None),ChrSets.Hex)
##    print(request.POST.dict())
##    print(verify_employee_webhook)
##    print(employee_id)
##    print(buisness_id)
    if verify_employee_webhook and employee_id and buisness_id and api_key:
        my_database = mysql.connector.connect(
          host=DBCREDS[0],
          user=DBCREDS[1],
          password=DBCREDS[2],
          auth_plugin='mysql_native_password'
        )
        mycursor = my_database.cursor()
        
        mycursor.execute("SELECT * FROM impersa_no.buisness WHERE `id` = "+str(int(buisness_id)))
        
        if mycursor.fetchall()[0][2] == api_key:
            mycursor.execute("SELECT * FROM impersa_no.verifications")
            verify_list_existing = mycursor.fetchall()
            customer_tokens_existing = []
            employee_tokens_existing = []
            verifier_tokens_existing = []
            for i in verify_list_existing:
                customer_tokens_existing.append(i[10])
                employee_tokens_existing.append(i[11])
                verifier_tokens_existing.append(i[12])
            customer_token = uuid.uuid4().hex
            while customer_token in customer_tokens_existing:
                customer_token = uuid.uuid4().hex
            employee_token = uuid.uuid4().hex
            while employee_token in employee_tokens_existing:
                employee_token = uuid.uuid4().hex
            verifier_token = uuid.uuid4().hex
            while verifier_token in verifier_tokens_existing:
                verifier_token = uuid.uuid4().hex
            customer_link = WORKING_URL+"/customer_check?token="+customer_token
            employee_link = WORKING_URL+"/employee_check?token="+employee_token
            verifier_link = WORKING_URL+"/verifier_check?token="+verifier_token
            
            mycursor.execute(
                "INSERT INTO impersa_no.verifications "+
                "(buisness_id,employee_id,customer_link,employee_link,"+
                "customer_allowed,employee_clip,verifier_allowed,verifier_link,verifier_ready,"+
                "customer_token,employee_token,verifier_token,created) "+
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (int(buisness_id),int(employee_id),customer_link,employee_link,
                 None,None,None,verifier_link,verify_employee_webhook,
                 customer_token,employee_token,verifier_token,time.time())
            )
            my_database.commit()
            
            response = json.dumps({
                "customer":customer_link,
                "employee":employee_link
                })
            return HttpResponse(response)
        else:
            return HttpResponse("error",status=400)
    else:
        return HttpResponse("error",status=400)


