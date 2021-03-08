from django.shortcuts import render
import uuid
import random
from .models import Employee,Customer_department
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
import http.client
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache

#auth_token = str(uuid.uuid4())

# Create your views here.

CACHE_TTL = getattr(settings ,'CACHE_TTL' , DEFAULT_TIMEOUT)


def emp_login(request):
    if request.method=='POST':
        employee_id = request.POST.get('employeeid')
        password = request.POST.get('password')
        request.session['employeeid']=employee_id
        request.session['password']=password


        try:
            user_obj = Employee.objects.get(employee_id = request.session['employeeid'],password=request.session['password'])

            if not user_obj.is_verified:
                messages.success(request, 'Profile is not verified check your mail.')
                return redirect('/emp_login')
            else:
                return render(request,'dash.html',{'user_obj':user_obj})

        except Employee.DoesNotExist:
            messages.success(request, 'Employee ID and Password Does Not MAtched.')
            return redirect('/emp_login')
    
  

    
    return render(request,'login.html')


def employee_profile_view(request):
    user_obj = Employee.objects.get(employee_id = request.session['employeeid'],password=request.session['password'])
    return render(request,'emp_profile.html',{'user_obj':user_obj})

def employee_logout(request):
    try:
        del request.session['employeeid']
        del request.session['password']

    except KeyError:
        pass

    return render(request, 'login.html')


# def employee_dashboard(request):
#     return render(request, 'dash.html')


def customer_register(request):
    return render(request,'customer_register.html',{'customer':Customer_department.objects.all(),'emp':Employee.objects.all()})


def register(request):  # employeee register
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        user_name = request.POST.get('uname')
        email = request.POST.get('email')
        mobile = request.POST.get('mnumber')
        #request.sessions['mobile']=mobile
        auth_token = str(uuid.uuid4())
        employee_id = 'wealth'+'{:06d}'.format(random.randrange(1, 999999))
        password=request.POST.get('password')
        employee=Employee(first_name=first_name,last_name=last_name,user_name=user_name,email=email,mobile=mobile,auth_token=auth_token,employee_id=employee_id,password=password)
        employee.save()
        send_mail_after_registration(email , auth_token)
        otp = str(random.randint(1000 , 9999))
        send_otp(mobile, otp)
        return redirect('/token')
        
    return render(request,'reg.html')


def success(request):
    return render(request , 'success.html')


def token_send(request): 
    return render(request , 'token.html')


def verify(request , auth_token): # email is verifing
    try:
        profile_obj = Employee.objects.filter(auth_token = auth_token).first()
        
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/emp_login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified and Password sent to register Email to check.')
            send_mail_password(profile_obj.email, profile_obj.employee_id, profile_obj.password)
            return redirect('/emp_login')
        else:
            return HttpResponse("your account is not there in database")
    except Exception as e:
        print(e)
        return HttpResponse("home")


def send_mail_after_registration(email , token): # send mail verified
    print('sending email')
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list)


def send_mail_password(email ,employee_id, password): # password and employeeid send to mail
    subject = 'Employee Password to Login'
    message = "Employee ID"+" "+employee_id+"\n"+"Acoount Password to login"+" "+password
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list)


def send_otp(mobile , otp):
    print("FUNCTION CALLED")
    print(otp)
    print(mobile)
    # conn = http.client.HTTPSConnection("api.msg91.com")
    # authkey = "241022AVD5q0z2z5bb5d749" 
    # headers = { 'content-type': "application/json" }
    # url = "http://control.msg91.com/api/sendotp.php?otp="+otp+"&message="+"Your otp is "+otp +"&mobile="+mobile+"&authkey="+authkey+"&country=91"
    # conn.request("GET", url , headers=headers)
    # res = conn.getresponse()
    # data = res.read()
    # print(data)
    # return None
    conn = http.client.HTTPSConnection("api.msg91.com")
    payload = '''{  
        "sender":"MSGIND",
        "route":"4",
        "country":"91",
        "flash":1,
        "sms":[
            {  
                    "message":"http://127.0.0.1:8000/sms-verfify",
                    "to":["7259837437"]
            }
        ]
    }'''

    headers = {
        'authkey': "241022AVD5q0z2z5bb5d749",
        'content-type': "application/json"
    }

    conn.request("POST", "/api/v2/sendsms?country=91", payload, headers)

    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return HttpResponse(data.decode("utf-8"))


def customer_accepted(request):      # customer accepted  form
    return render(request,'cust_acee.html')


def customer_rejected(request):   #customer rejected form
    return render(request,'cust_reject.html')


def get_all_employee_data(request):
    data=Employee.objects.all()
    return render(request, 'emp_data.html', {'data':data})


def get_employee_data_by_id(request, id):

    if cache.get(id):
        employee = cache.get(id)
        print("Data from Cache")

    else:

        try:
            employee = Employee.objects.get(id=id)
            cache.set(id,employee)
            print("data from database")

        except Employee.DoesNotExist:

            return redirect("/get_all_employee_data")

    return render(request, 'emp_by_id.html',{'a':employee})
    