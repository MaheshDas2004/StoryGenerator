from django.shortcuts import render

# Create your views here.
def signup(request):
    if request.method=="POST":
        firstname=request.POST.get("firstname")
        lastname=request.POST.get("lastname")
        email=request.POST.get("email")
        password=request.POST.get("password")
        cfpassword=request.POST.get("confirmpassword")

        if password != cfpassword:
            return render(request,"accounts/signup.html",{"error":"Passwords do not Match enter password again"})
    return render(request,"accounts/signup.html")
def login(request):
    if request.method=="POST":
        username=request.POST.get
    return render(request,"accounts/login.html")