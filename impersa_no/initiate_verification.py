from django.http import HttpResponse
import json
import mysql.connector

def initiate_verification(request):
    verifying_employee_webhook = request.GET.get("verify_employee_webhook",None)
    employee_id = request.GET.get("employee_id",None)
    company_id = request.GET.get("company_id",None)
    if verifying_employee_webhook and employee_id and company_id:
        response = json.dumps({
            "customer":customer_link,
            "employee":employee_link
            })
        return HttpResponse(response)
    else:
        return HttpResponse("error",status=400)
