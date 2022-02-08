from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
def register(request):
    if request.method== "POST":
        form =  RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email        = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            #user activation
            current_site = get_current_site(request)
            mail_subject = "pleace activate your account"
            messages = render_to_string('accounts/account_varification_email.html', {
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, messages, to=[to_email])
            send_email.send()
            # messages.success(request, 'Thank you for registering with us. We have sent you a varification email to your email address. please varify it.')
            return redirect('/account/login/?command=varification&email='+email)
    else:
        form = RegistrationForm()
    
    context={
        'form': form,
    }
    return render(request, 'accounts/register.html', context )

def login(request):
    if request.method == 'POST':
        email= request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect('dashboard')
        
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url ='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'you are logged out.')
    return redirect('login')

def activate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError,Account.DoesNotExist):
        user =None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active= True 
        user.save()
        messages.success(request, 'Congratulation! Your account is activated')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')
@login_required(login_url = 'login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def forgotpassword(request):
    if request.method =="POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user= Account.objects.get(email__exact=email)
            
            #Reset password email
            current_site = get_current_site(request)
            mail_subject = "Reset Your Password"
            messages = render_to_string('accounts/reset_password_email.html', {
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, messages, to=[to_email])
            send_email.send()
           # messages.success(request, 'password reset email has been sent to your email address.')
           
            return redirect('login')

        else:
            messages.error(request, 'Account does not exists')
            return redirect('forgotpassword')
    return render(request, 'accounts/forgotpassword.html')

def resetpassword_validate(request,uidb64, token):
         try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account._default_manager.get(pk=uid)
         except(TypeError, ValueError, OverflowError,Account.DoesNotExist):
            user =None

         if user is not None and default_token_generator.check_token(user, token):
            request.session['uid'] = uid
            messages.success(request , 'pleace resert your password')
            return redirect('resetpassword')
         else:
            messages.error(request, 'This link has been expired')
            return redirect('login')

def resetpassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_passsword:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('resetpassword')
    else:
       return render(request, 'accounts/resetpassword.html')
