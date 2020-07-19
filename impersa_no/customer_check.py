from django.http import HttpResponse

WORKING_URL = open("WORKING_URL.txt").read()

def customer_check(request):
    token = request.POST.get("token",None)
    if token:
        return HttpResponse("")
    else:
        return HttpResponse("error",status=400)
