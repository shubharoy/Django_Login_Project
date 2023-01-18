from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail  
#from django.db.models import Q
  

# Create your views here....
#This function is use for Website homepage
def home(request):     
    return render(request, "index.html")

#Forgot Password Page & Send New Password by email
@csrf_exempt
def ForgotPassword(request):    
    if request.method == "POST":      
        user_email = request.POST.get('useremail')  
        
        try:
            #Get User list by email address
            useremail = User.objects.get(email =user_email)
        except:
            messages.error(request, 'Email Does not Exist')
            return render(request, "forgotpassword.html")

        if useremail is not None:
            #User.objects.filter(email = email).update(first_name = firstname)
            new_password = "Admin123456"
            useremail.set_password(new_password)
            useremail.save()  
            sendEmail = send_mail(
                'Password Change Information',
                'Hi, Your New Password Is : '+new_password,
                'settings.EMAIL_HOST_USER',
                [user_email],
                fail_silently = False
            )

            #Informing user that the email send successfully or not
            if sendEmail:
                messages.success(request, "Send New Password Successfully")
            else:
                messages.error(request, "Email Not Sent!! Try again")
            return redirect('/home')    
                
    return render(request, "forgotpassword.html") 


#Login Request after giving username & Password
@csrf_exempt
def requestLogin(request):
    #Check Is the user already loggedin or not
    if request.user.is_authenticated:
        return redirect('/userindex')
        
    if request.method == "POST":
        userName = request.POST.get('username')
        passWord = request.POST.get('password')

        try:
            #Get User list by username
            User.objects.get(username =userName)  
        except:
            try:
                #Get User list by Email
                User.objects.get(email =userName) 
            except:
                messages.error(request, 'User Does not Exist')
                return render(request, "index.html")

        #Checking given login information By- Username Or Email 
        user = authenticate(request, username=userName, password=passWord)
         
        if user is not None:
            login(request, user)
            #return redirect('/userindex')
        else:
            messages.error(request, 'Username or Passsword Not Match ')
            
    return render(request, "index.html")


#Function use for logout the user
def logoutUser(request):
    logout(request)
    return redirect('loginapp:home')

#After login User Home Page
@login_required(login_url='loginapp:requestLogin')
def userindex(request):   
    #Get All User Information
    GetUserList = User.objects.all()    
    context = {'GetUserList' : GetUserList} 
    return render(request, "home_user.html", context)

#User can change password by this function
@login_required(login_url='loginapp:requestLogin')
@csrf_exempt
def changepassword(request):   
    if request.method == "POST":
         passWord = request.POST.get('password')
         new_password = request.POST.get('new_password')
         confirm_password = request.POST.get('confirm_password')

        #Checking the user is logged in or not..
         if request.user.is_authenticated:
            #If new password & confirm password match than password will be change successfully
            if new_password == confirm_password:
                current_user = User.objects.get(email=request.user.email)                              
                current_user.set_password(new_password)
                
                #If current & new password match than password will be change successfully 
                #Both password encrypted here & its managed by set_password function
                if (current_user.set_password(new_password) == current_user.set_password(passWord)):
                    current_user.save()    
                    messages.success(request, "Your password has been changed")
                else:
                    messages.error(request, "Current Password and New Password nat match!! Try again")
            else:
                messages.error(request, 'New & Confirm Password Not Match !!')

    return render(request, "change_password.html")


def error_404(request, exception):   
    return render(request, '404.html')