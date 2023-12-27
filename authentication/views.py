from base64 import urlsafe_b64decode, urlsafe_b64encode
from email.message import EmailMessage
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect,render
from django.contrib.auth import authenticate,login,logout
from login import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token 
from .models import Article

# Create your views here.

def home(request):
    return render(request,"authentication/index.html")

def signup(request):

    if request.method == "POST":

        fname= request.POST['fname']
        lstname= request.POST['lstname']
        uname= request.POST['uname']
        email= request.POST['email']
        pass1= request.POST['pass1']
        pass2= request.POST['pass2']

        if User.objects.filter(username = uname):
            messages.error(request,"Username already exists! Please try another username.")
            return redirect('home')
        
        if User.objects.filter(email = email):
            messages.error(request,"Email already registered!")
            return redirect('home')
        
        if len(uname)>10:
            messages.error(request,"Username must be under 10 characters!")

        if pass1 != pass2:
            messages.error(request,"Password didn't match!!")

        if not uname.isalnum():
            messages.error(request,"Username must be Alpha-numeric!")
            return redirect('home')
        
        
        myuser = User.objects.create_user(uname, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lstname
        
        myuser.save()

        messages.success(request, "Your  account has been successfully created!.\n We have sent you a confirmation email,please confirm your email in order to activate your account.")
        
        #Welcome Email

        subject = "Welcome CodestreetFinance!!!"
        message= "Hello" + myuser.first_name + "! \n" + "Thankyou for visiting our website.Get ready to dive into the most dynamic and ever growing field of Finance combnined with code. \n We have also sent you an email address,please confirm your email address in order to activate your account. \n\n Thankyou \n\n CodestreetFinance."
        from_email= settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)
        
        #Email address confirmation email
        current_site=get_current_site(request)
        email_subjects="Confirm your email @CodestreetFinance - Login!"
        message2= render_to_string('email_confirmation.html'),{
            'name': myuser.first_name,
            'domain':current_site.domain,
            'uid': urlsafe_b64encode(force_bytes(myuser.pk)),
            'token':generate_token.make_token(myuser)
        }
        email = EmailMessage(
            email_subjects,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('signin')
    

    
    return render(request,"authentication/signup.html")

def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')


def signin(request):

    if request.method== 'POST':
        uname= request.POST['uname']
        pass1=request.POST['pass1']
        

        user=authenticate(username=uname,password=pass1)

        if user is not None:
            login(request,user)
            fname=user.first_name
            return render(request,'authentication/index.html',{'fname':fname})
    
        else:
            messages.error(request,"Bad Credentials")
            return redirect('home')


    return render(request,"authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Loggeg out sucessfully!")
    return redirect('home')




def contactus(request):
    return render(request,'authentication/contactus.html')
    #return redirect('home')

def about(request):
    return render(request,'authentication/about.html')

def webinar(request):
    return render(request,'authentication/webinar.html')

def posts(request):
    return render(request,'authentication/posts.html')

from django.shortcuts import render
from .models import Article
from django.http import HttpResponse

# Create your views here.
def list_of_articles(request):
    articles = Article.publishedArticles.all()
    

    
    return render(request, 'authentication/list.html', {'articles': articles})
    
# articles/views.py
from django.views.generic import DetailView
from .models import Article

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'authentication/article_detail.html'
    context_object_name = 'article'
