from django.db.models.constraints import UniqueConstraint
from django.shortcuts import redirect, render
from .models import Company_Customer, Company_Product, Company_data, Customer_Order
# Create your views here.

import smtplib
import random
import email.message
from datetime import timedelta, date ,datetime
# -------------------------------------- Company -----------------------------------------

def login(request):
    if 'comp_data' in request.session.keys() or 'lock' in request.session.keys():
        if 'comp_data' in request.session.keys():
            obj = Company_data.objects.get(id = request.session['comp_data'])    
            del request.session['comp_data']
        elif 'lock' in request.session.keys():
            obj = Company_data.objects.get(id = request.session['lock'])
        request.session['lock'] = obj.id
        return redirect('lockscreen')
    else:
        err = ''
        if request.POST:
            em = request.POST['em1']
            pass1 = request.POST['pass']

            try:
                obj = Company_data.objects.get(com_em = em)
                if obj.com_pass == pass1:
                    request.session['comp_data'] = obj.id
                    return redirect('dashboard')
                else:
                    err = 'Wrong Password !!'
            except:
                err = 'Email not Registered !!'
        return render(request,'company/login/login.html',{'error':err})

def register(request):
    err = ''
    if request.POST:
        name = request.POST['nm1']
        em = request.POST['em1']
        pass1 = request.POST['pass']
        pass2 = request.POST['re_pass']

        try:
            var = Company_data.objects.get(com_em = em)
            err = "Email already Registered"
        except:
            if pass1 == pass2:
                obj = Company_data()
                obj.com_nm = name
                obj.com_em = em
                obj.com_pass = pass2
                obj.save()
                return redirect('login')
            else:
                err = "Password doesn't match"
    return render(request,'company/login/register.html',{'error':err})

def forgotpassword(request):
    err = ''
    if request.POST:
        em = request.POST['em1']

        try:
            err = 'Email not registered !!'
            var = Company_data.objects.get(com_em = em)

            err = 'Internet disconnected !!'
            sender_email = "getpaswordback@gmail.com"
            pass1 = "Demo@123"
            receiver_email = em
            receiver_name = var.com_nm
            server = smtplib.SMTP('smtp.gmail.com',587)

            #-----------OTP------------
            otp = ''
            for i in range(6):
                otp += str(random.randint(0,9))
            print(otp)
            #-----------OTP------------

            err = 'Error sending OTP'
            message1 = f"""
            Hey Mr. {receiver_name}
            Your OTP for the recovery of your Account
            OTP: {otp}
            Do not Share your OTP with anyone.
            Thanks for being with us.


            This is from AdminLAB Corp.
            """
            msg = email.message.Message()
            msg['subject'] = "Recover your Account"
            msg.add_header('Content-Type','text/plain')
            msg.set_payload(message1)

            server.starttls()
            server.login(sender_email,pass1)
            server.sendmail(sender_email,receiver_email,msg.as_string())

            request.session['otp'] = otp
            request.session['new_user'] = var.id
            return redirect('otp')

        except Exception as e:
            print(e)
    return render(request,'company/login/forgotpassword.html',{'error':err})

def otp(request):
    if 'otp' in request.session.keys():
        err = ''
        if request.POST:
            user_otp = request.POST['otp']
            otp1 = request.session['otp']

            if str(user_otp) == str(otp1):
                del request.session['otp']
                print('ready for new password change')
                return redirect('changepassword')
            else:
                err = 'Incorrect OTP !!'
        else:
            return render(request,'company/login/otp.html',{'error':err})
    else:
        return redirect('login')

def changepassword(request):
    if 'new_user' in request.session.keys():
        err = ''
        if request.POST:
            pass1 = request.POST['pass']
            pass2 = request.POST['re_pass']
            
            if pass1 == pass2:
                obj = Company_data.objects.get(id = int(request.session['new_user']))
                obj.com_pass = pass2
                obj.save()
                del request.session['new_user']
                return redirect('login')
            else:
                err = "Password doesn't match"
        else:
            User = Company_data.objects.get(id = int(request.session['new_user']))
            return render(request,'company/login/changepassword.html',{'Users':User,'error':err})
    else:
        return redirect('login')

def dashboard(request):
    if 'comp_data' in request.session.keys():
        User = Company_data.objects.get(id = int(request.session['comp_data']))
        print(User)
        return render(request,'company/dash/dashboard.html',{'Users':User})
    else:
        return redirect('login')

def logout(request):
    if 'comp_data' in request.session.keys():
        del request.session['comp_data']
        return redirect('login')
    else:
        print('session not found')

def profile(request):
    if 'comp_data' in request.session.keys():
        User = Company_data.objects.get(id = int(request.session['comp_data']))
        if request.POST:
            nm = request.POST['nm1']
            em = request.POST['em1']
            cno = request.POST['cno']
            pass1 = request.POST['pass1']
            add1 = request.POST['add']
            prof1 = request.FILES.get('prof1')
            
            User.com_nm = nm
            User.com_em = em
            User.com_cno = cno
            User.com_pass = pass1
            User.com_add = add1
            if prof1 != None:
                User.profile = prof1
            User.save()
        return render(request,'company/dash/profile.html',{'Users':User})
    else:
        return redirect('login')

def add_customer(request):
    if 'comp_data' in request.session.keys():
        User = Company_data.objects.get(id = int(request.session['comp_data']))
        err = ''
        if request.POST:
            nm = request.POST['nm1']
            em = request.POST['em1']
            cno = request.POST['cno']
            add1 = request.POST['add1']
            prof1 = request.FILES.get('prof1')

            try:
                
                err = 'Internet Disconnected !!'
                sender_email = "getpaswordback@gmail.com"
                pass1 = "Demo@123"
                receiver_email = em
                server = smtplib.SMTP('smtp.gmail.com',587)

                #-----------OTP------------
                otp = ''
                for i in range(8):
                    otp += str(random.randint(0,9))
                print(otp)
                #-----------OTP------------

                err = 'Error Sending OTP'
                message1 = f"""
                Hey Mr. {nm}
                You are Successfully registered to {User.com_nm}

                Your Login Credentials are below
                Email: {em}
                Password: {otp}

                You can login here -> http://127.0.0.1:8000/customer_login/
                Do not Share your Credentials with anyone.
                Thanks for being with us.


                This is from {User.com_nm}
                """
                msg = email.message.Message()
                msg['subject'] = "Welcome Customer"
                msg.add_header('Content-Type','text/plain')
                msg.set_payload(message1)

                server.starttls()
                server.login(sender_email,pass1)
                server.sendmail(sender_email,receiver_email,msg.as_string())

            except Exception as e:
                print(e)

            obj = Company_Customer()
            obj.cust_nm = nm
            obj.cust_em = em
            obj.cust_cno = cno
            obj.cust_pass = otp
            obj.cust_add = add1
            obj.comp = User
            if prof1 != None:
                obj.cust_profile = prof1
            obj.save()
            return redirect('view_customer')
        return render(request,'company/dash/add_customer.html',{'Users':User,'error':err})
    else:
        return redirect('login')

def view_customer(request):
    if 'comp_data' in request.session.keys():
        User = Company_data.objects.get(id = int(request.session['comp_data']))
        obj = Company_Customer.objects.filter(comp = User)
        return render(request,'company/dash/view_customer.html',{'Users':User,'obj':obj})
    else:
        return redirect('login')

def delete_customer(request,id):
    if 'comp_data' in request.session.keys():
        User = Company_data.objects.get(id = int(request.session['comp_data']))
        custs = Company_Customer.objects.get(id = id)
        custs.delete()
        return redirect('view_customer')
    else:
        return redirect('login')

def update_customer(request,id):
    if 'comp_data' in request.session.keys():
        User = Company_data.objects.get(id = int(request.session['comp_data']))
        custs =Company_Customer.objects.get(id=id)
        err = ''
        if request.POST:
            nm = request.POST['nm1']
            em = request.POST['em1']
            cno = request.POST['cno']
            add1 = request.POST['add1']
            prof1 = request.FILES.get('prof1')
            pass1 = request.POST['pass1']

            custs.cust_nm = nm
            custs.cust_em = em
            custs.cust_cno = cno
            custs.cust_add = add1
            custs.cust_pass = pass1
            if prof1 != None:
                custs.cust_profile = prof1
            custs.save()
            return redirect('view_customer')
        return render(request,'company/dash/update_customer.html',{'Users':User,'customer':custs,'error':err})
    else:
        return redirect('login')

def view_order(request):
    if 'comp_data' in request.session.keys():
        User = Company_data.objects.get(id = int(request.session['comp_data']))
        obj = Customer_Order.objects.filter(comp = User,status='pending')
        return render(request,'company/dash/view_order.html',{'Users':User,'obj':obj})
    else:
        return redirect('login')

def order_accepted(request,id):
    if 'comp_data' in request.session.keys():
        obj = Customer_Order.objects.get(id = id)
        obj1 = Company_Product.objects.get(id = obj.pro.id)
        obj.status = 'accepted'
        obj.save()
        obj1.pro_qty = int(int(obj1.pro_qty) - int(obj.qty))
        obj1.save()
        return redirect('view_order')
    else:
        return redirect('login')

def order_rejected(request,id):
    if 'comp_data' in request.session.keys():
        obj = Customer_Order.objects.get(id = id)
        obj.status = 'rejected'
        obj.save()
        return redirect('view_order')
    else:
        return redirect('login')

def view_accepted_order(request):
    if 'comp_data' in request.session.keys():
        User = Company_data.objects.get(id = int(request.session['comp_data']))
        obj = Customer_Order.objects.filter(comp = User,status='accepted')
        cust1 = Company_Customer.objects.filter(comp = User,customer__status='accepted').distinct()
        return render(request,'company/dash/view_accepted_order.html',{'Users':User,'obj':obj,'cust1':cust1})
    else:
        return redirect('login')

def order_list_p(request,id):
    if 'comp_data' in request.session.keys():
        User = Company_data.objects.get(id = int(request.session['comp_data']))
        cust1 = Company_Customer.objects.get(id = id)
        obj = Customer_Order.objects.filter(cust = id,status='accepted')
        sum1 = 0
        for i in obj:
            sum1 += i.total_price
        print(sum1)
        return render(request,'company/dash/order_list_personal.html',{'Users':User,'cust1':cust1,'ord':obj,'total':sum1})
    else:
        return redirect('login')

def invoice(request,id):
    if 'comp_data' in request.session.keys():
        User = Company_data.objects.get(id = int(request.session['comp_data']))
        print(User)
        date2 = date.today()
        date1 = date2.strftime("%d/%m/%y")
        duedate = date.today() + timedelta(days=15)
        duedate = duedate.strftime("%d/%m/%y")
        cust1 = Company_Customer.objects.get(id = id)
        obj = Customer_Order.objects.filter(cust = id,status='accepted')
        sum1 = 0
        for i in obj:
            sum1 += i.total_price
        tax = round((sum1*9.3)/100,2)
        shipping = 5.80
        total = round(sum1 + tax + shipping,2)
        return render(request,'company/dash/invoice.html',{'Users':User,'date':date1,'duedate':duedate,'cust1':cust1,'obj':obj,'subtotal':sum1,'tax':tax,'total':total})
    else:
        return redirect('login')

def invoice_print(request,id):
    if 'comp_data' in request.session.keys():
        User = Company_data.objects.get(id = int(request.session['comp_data']))
        print(User)
        date2 = date.today()
        date1 = date2.strftime("%d/%m/%y")
        duedate = date.today() + timedelta(days=15)
        duedate = duedate.strftime("%d/%m/%y")
        cust1 = Company_Customer.objects.get(id = id)
        obj = Customer_Order.objects.filter(cust = id,status='accepted')
        sum1 = 0
        for i in obj:
            sum1 += i.total_price
        tax = round((sum1*9.3)/100,2)
        shipping = 5.80
        total = round(sum1 + tax + shipping,2)
        return render(request,'company/dash/invoice_print.html',{'Users':User,'date':date1,'duedate':duedate,'cust1':cust1,'obj':obj,'subtotal':sum1,'tax':tax,'total':total})
    else:
        return redirect('login')

def lockscreen(request):
    if 'lock' in request.session.keys():
        obj = Company_data.objects.get(id = request.session['lock'])
        err = ''
        if request.POST:
            pass1 = request.POST['pass1']
            if pass1 == obj.com_pass:
                request.session['comp_data'] = obj.id
                del request.session['lock']
                return redirect('dashboard')
            else:
                err = 'Wrong Password !!'
    return render(request,'company/login/lockscreen.html',{'Users':obj,'error':err})

def locklogout(request):
    if 'lock' in request.session.keys():
        del request.session['lock']
    return redirect('login')

# -------------------------------------- Company -----------------------------------------

# -------------------------------------- Customer -----------------------------------------

def customer_login(request):
    if request.POST:
        em = request.POST['email']
        pass1 = request.POST['pass']

        try:
            obj = Company_Customer.objects.get(cust_em = em)
            if obj.cust_pass == pass1:
                request.session['customer_login'] = obj.id
                return redirect('customer_dashboard')
            else:
                print('password is wrong')
        except:
            print('email is wrong')
    return render(request,'customer/login/login.html')

def customer_dashboard(request):
    if 'customer_login' in request.session.keys():
        obj = Company_Customer.objects.get(id = request.session['customer_login'])
        prod = Company_Product.objects.filter(comp = obj.comp)
        return render(request,'customer/dash/dashboard.html',{'prod':prod})
    else:
        return redirect('customer_login')

def customer_contact(request):
    if 'customer_login' in request.session.keys():
        return render(request,'customer/dash/contact.html')
    else:
        return redirect('customer_login')

def customer_order(request):
    if 'customer_login' in request.session.keys():
        obj = Company_Customer.objects.get(id = request.session['customer_login'])
        ord = Customer_Order.objects.filter(cust = obj)
        return render(request,'customer/dash/all_orders.html',{'ord':ord,'obj':obj})
    else:
        return redirect('customer_login')

def customer_profile(request):
    if 'customer_login' in request.session.keys():
        obj = Company_Customer.objects.get(id = request.session['customer_login'])
        if request.POST:
            nm = request.POST['nm1']
            em = request.POST['em1']
            cno = request.POST['cno']
            add1 = request.POST['add1']
            img1 = request.FILES.get('img1')
            pass1 = request.POST['pass1']

            obj.cust_nm = nm
            obj.cust_em = em
            obj.cust_cno = cno
            obj.cust_add = add1
            obj.cust_pass = pass1
            if img1 != None:
                obj.cust_profile = img1
            obj.save()
        return render(request,'customer/dash/profile.html',{'obj':obj})
    else:
        return redirect('customer_login')

def customer_logout(request):
    if 'customer_login' in request.session.keys():
        del request.session['customer_login']
        return redirect('customer_login')
    else:
        return redirect('customer_login')

def place_order(request,id):
    if 'customer_login' in request.session.keys():
        obj = Company_Customer.objects.get(id = request.session['customer_login'])
        prod = Company_Product.objects.get(id = id)
        if request.POST:
            qty = request.POST['qty2']
            if int(qty) > int(prod.pro_qty):
                error1 = 'Quantity out of range'
                return render(request,'customer/dash/place_order.html',{'prod':prod,'error':error1})
            else:
                or1 = Customer_Order()
                or1.comp = obj.comp
                or1.cust = obj
                or1.pro = prod
                or1.qty = int(qty)
                or1.total_price = int(int(qty)*int(prod.pro_pr))
                or1.save()
                return redirect('customer_dashboard')
        return render(request,'customer/dash/place_order.html',{'prod':prod})
    else:
        return redirect('customer_login')

# -------------------------------------- Customer -----------------------------------------

# -------------------------------------- Product -----------------------------------------

def add_product(request):
    if 'comp_data' in request.session.keys():
        User = Company_data.objects.get(id = int(request.session['comp_data']))
        print(User)
        if request.POST:
            nm = request.POST['nm1']
            pr1 = request.POST['pr1']
            qty1 = request.POST['qty1']
            img1 = request.FILES.get('img1')

            obj = Company_Product()
            obj.pro_nm = nm
            obj.pro_pr = pr1
            obj.pro_qty = qty1
            obj.comp = User
            if img1 != None:
                obj.pro_img = img1
            obj.save()
            return redirect('view_product')
        return render(request,'company/dash/add_product.html',{'Users':User})
    else:
        return redirect('login')

def view_product(request):
    if 'comp_data' in request.session.keys():
        User = Company_data.objects.get(id = int(request.session['comp_data']))
        print(User)
        prod = Company_Product.objects.filter(comp = User)
        return render(request,'company/dash/view_product.html',{'Users':User,'product':prod})
    else:
        return redirect('login')

def update_product(request,id):
    if 'comp_data' in request.session.keys():
        User = Company_data.objects.get(id = int(request.session['comp_data']))
        obj = Company_Product.objects.get(id=id)
        print(User)
        if request.POST:
            nm = request.POST['nm1']
            pr1 = request.POST['pr1']
            qty1 = request.POST['qty1']
            img1 = request.FILES.get('img1')

            obj.pro_nm = nm
            obj.pro_pr = pr1
            obj.pro_qty = qty1
            if img1 != None:
                obj.pro_img = img1
            obj.save()
            return redirect('view_product')
        return render(request,'company/dash/update_product.html',{'Users':User,'product':obj})
    else:
        return redirect('login')

def delete_product(request,id):
    if 'comp_data' in request.session.keys():
        User = Company_data.objects.get(id = int(request.session['comp_data']))
        print(User)
        obj = Company_Product.objects.get(id=id)
        obj.delete()
        return redirect('view_product')
    else:
        return redirect('login')

# -------------------------------------- Product -----------------------------------------