from django.http import HttpResponse

def index(request):
    return HttpResponse("This is an api. Go to impersa-no.maxstuff.net to learn more.")
