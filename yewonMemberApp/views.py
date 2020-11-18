from django.shortcuts import render, redirect
from .models import Customer, Newsletter
from django.contrib import messages
import bcrypt
from django.db.models import Count
from django.conf import settings
from twilio.rest import Client

# Create your views here.
def index(request):
    return redirect('/main')
    
def main(request):
    return render(request, 'index.html')

def next(request):
    if request.method == "POST":
        customer_with_num = Customer.objects.filter(phone=request.POST['phone_num'])
        print(customer_with_num)
        if len(customer_with_num) > 0:
            customer = customer_with_num[0]
        else:
            customer = Customer.objects.create(phone=request.POST['phone_num'])
        request.session['customer_id'] = customer.id
        return redirect('/customer/dashboard') #the main page of the application
    return redirect(request, '/')

def dashboard(request):
    if 'customer_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    customer_to_view = Customer.objects.get(id=request.session['customer_id'])
    remaining_pts = 100 - customer_to_view.points
    context = {
        'customer': customer_to_view,
        'remaining_pts': remaining_pts,
    }
    return render(request, 'dashboard.html', context)

def addpoints(request):
    if 'customer_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    if request.POST['purchase_amount'] == '':
        messages.error(request, "Cannot add $0")
        return redirect('/customer/logindash')
    customer_to_update = Customer.objects.get(id=request.session['customer_id'])
    customer_to_update.points += int(request.POST['purchase_amount'])/100
    customer_to_update.save()
    return redirect('/customer/dashboard')

def addpoints2(request):
    if 'customer_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    print(request.POST['purchase_amount'])
    if request.POST['purchase_amount'] == '':
        messages.error(request, "Cannot add $0")
        return redirect('/customer/logindash')
    customer_to_update = Customer.objects.get(id=request.session['customer_id'])
    customer_to_update.points += int(request.POST['purchase_amount'])/100
    customer_to_update.save()
    return redirect('/customer/logindash')

def loginpage(request):
    if 'customer_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    customer_to_view = Customer.objects.get(id=request.session['customer_id'])
    context = {
        'customer': customer_to_view,
    }
    return render(request, 'loginpage.html', context)

def register(request):
    if request.method == "POST":
        errors = Customer.objects.update_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/customer/loginpage')
        else:
            #Register an account for our Customer
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            # print(hashed_pw)
            customer_to_update = Customer.objects.get(id=request.session['customer_id'])
            customer_to_update.name = request.POST['name']
            customer_to_update.email = request.POST['email']
            customer_to_update.password = hashed_pw
            customer_to_update.save()
            request.session['customer_id'] = customer_to_update.id
            return redirect('/customer/dashboard') #the main page of the application
    return redirect(request, '/')

def login(request):
    print("debug login1")
    if request.method == "POST":
        errors = Customer.objects.login_validator(request.POST)
        print("debug login2")
        if len(errors) > 0:
            print("debug login3")
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/customer/loginpage')
        else:
            print("debug login4")
            customer = Customer.objects.filter(phone=request.POST['phone_num'])
            if len(customer) > 0:
                customer = customer[0]
                print("debug login5")
                print(customer.name)
                if bcrypt.checkpw(request.POST['password'].encode('utf-8'), customer.password.encode()):
                    print("debug login5")
                    print(request.session['customer_id'])
                    print(customer.id)
                    request.session['customer_id'] = customer.id
                    return redirect('/customer/logindash')
    return redirect('/customer/logindash')

def logout(request):
    request.session.clear()
    return redirect('/')


def logindash(request):
    if 'customer_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    context = {
        'customer': Customer.objects.get(id=request.session['customer_id']),
        'all_news': Newsletter.objects.order_by('-created_at')
    }
    return render(request, 'logindash.html', context)

def edit(request, id):
    context = {
        "customer": Customer.objects.get(id=id)
    }
    return render(request, 'customeredit.html', context)

def adminedit(request, id):
    if 'customer_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    current_user = Customer.objects.get(id=request.session['customer_id'])
    context = {
        "customer": Customer.objects.get(id=id),
        "current_user": current_user
    }
    return render(request, 'adminedit.html', context)

def update(request, id):
    if request.method == "POST":
        errors = Customer.objects.update_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/customer/edit/'+str(id))
        print('debug update')
        print(request.POST.get('text_sub'))
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        customer_to_update = Customer.objects.get(id=id)
        customer_to_update.phone = request.POST['phone_num']
        customer_to_update.name = request.POST['name']
        customer_to_update.email = request.POST['email']
        customer_to_update.password = hashed_pw
        if request.POST.get('email_sub') == 'on':
            customer_to_update.newsletter_email = True
        else:
            customer_to_update.newsletter_email = False
        if request.POST.get('text_sub') == 'on':
            print("texttrue")
            customer_to_update.newsletter_text = True
        else:
            print("textfalse")
            customer_to_update.newsletter_text = False
        customer_to_update.save()
    return redirect('/customer/edit/'+str(id))

def manage_newsletter(request):
    if 'customer_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    context = {
        'customer': Customer.objects.get(id=request.session['customer_id']),
        'all_news': Newsletter.objects.order_by('-created_at')
    }
    return render(request, 'newsletters.html', context)

def add_newsletter(request):
    if request.method == "POST":
        errors = Newsletter.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            news = Newsletter.objects.create(title=request.POST['title'], content=request.POST['content'])
            message_to_broadcast = news.content
            print("debug twilio")
            print(message_to_broadcast)
            print(settings.TWILIO_ACCOUNT_SID)
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            for recipient in settings.SMS_BROADCAST_TO_NUMBERS:
                if recipient:
                    client.messages.create(to=recipient,
                                        from_="+12059316160",
                                        body=message_to_broadcast)
    return redirect('/admin/manage_newsletter')

def manage_customers(request):
    if 'customer_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    context = {
        'customer': Customer.objects.get(id=request.session['customer_id']),
        'all_customers': Customer.objects.order_by('created_at')
    }
    return render(request, 'manage_customers.html', context)

def delete_cust(request, id):
    if 'customer_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        print(request.session['customer_id'])
        current_user = Customer.objects.get(id=request.session['customer_id'])
        customer_with_id = Customer.objects.filter(id=id)
        if len(customer_with_id) > 0:
            cust = customer_with_id[0]
            print("debug delete")
            if current_user.admin == True:
                cust.delete()
    return redirect('/admin/manage_customers')
