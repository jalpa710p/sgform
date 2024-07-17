from django.shortcuts import render, redirect
from .models import Sgform
from django.core.mail import EmailMessage
import random
import pandas as pd
import requests
def form(request):
    if request.method == "POST":
        # Extract form data
        usn = request.POST.get("username")
        phn = request.POST.get("phone")
        eml = request.POST.get("email")
        psd = request.POST.get("password")
        # Generate OTPs
        photp = random.randint(1000, 9999)
        print('phoneotp->', photp)
        emailotp = random.randint(1000, 9999)
        print('emailotp->', emailotp)
        request.session['email'] = eml
        print("email->", type(eml))
        print(usn, phn, eml, psd, eml, photp)
        # Store email OTP in session
        d ={'username': [usn],
            'phone': [phn],
             'email': [eml],
            'password': [psd],
            'photp': [photp],
            'emailotp': [emailotp]
            }
        df = pd.DataFrame(d)
        df.to_csv('media/data.csv', index=False)
        data = Sgform.objects.create(usn=usn,
                     phn=phn,
                     eml=eml,
                     psd=psd,
                     photp=photp,
                     emailotp=emailotp)
        data.save()
        # csv_file_path = "/media/data.csv"
        # csv_data = df.to_csv(index=False)
        # Send OTPs
        # send_phone_otp(phn, photp)
        # send_email_otp(eml, emailotp)
#         # print(responseotp["Status"]
        return redirect('otpcheck', f=1)  # Assuming 'otpcheck' is the name of your OTP verification view
    return render(request, 'form.html')

def otpcheck(request, f=0):
    # mobile = ''
    if request.method == "POST":
        otp1 = request.POST.get("otp1")
        otp2 = request.POST.get("otp2")
        otp3 = request.POST.get("otp3")
        otp4 = request.POST.get("otp4")
        user_otp = otp1 + otp2 + otp3 + otp4

        if request.method == "POST" and f==1:
            mobile = request.session.get('mobile')
            print("mobile->", mobile)
            user = Sgform.objects.filter(phn=mobile)
            # return render(request, 'otp.html', {'f': 1})
            return redirect('otpcheck', f=2)

        elif request.method == "POST" and f==2:
            email = request.session.get('email')
            user = Sgform.objects.filter(eml=email)
            email = request.session.get('email')
            if user_otp == str(Sgform.objects.get(eml=email).emailotp):
                return redirect('dashboard')
            else:
                # Handle incorrect OTP
                return render(request, 'otp.html', {'f': f, 'error': True})

    return render(request, 'otp.html', {'f': f})

def dashboard(request):
    return render(request, 'dashboard.html')


def table(request):
    obj = Sgform.objects.all()
    print(("data is ->", obj))
    return render(request, 'table.html', context={'data': obj})

def edit(request, id):
    data = Sgform.objects.get(id=id)
    if request.method == "POST":
        data.usn = request.POST.get("username")
        data.phn = request.POST.get("phone")
        data.eml = request.POST.get("email")
        data.psd = request.POST.get("password")
        data.save()
        data = Sgform.objects.all()
        return render(request, 'table.html', context={'data': data})
    return render(request, 'edit.html', context={'data': data})

def delete(request, id):
    Sgform.objects.get(id=id).delete()
    data = Sgform.objects.all()
    return render(request, 'table.html', context={'data': data})


def send_email_otp(email, emailotp):
    """
    Function to send OTP to the provided email address.
    """
    email = EmailMessage(
        subject='OTP for Email Verification',
        body=f'Your OTP is {emailotp}. Please use this to verify your email.',
        from_email='settings.EMAIL_HOST_USER',
        to=[email]
    )
    email.send()

def send_phone_otp(phone, photp):
    """
    Function to send OTP to the provided phone number.
    """
    # Your code for sending OTP via SMS to the provided phone number
    phn = "+91" + phone
    url = f'https://2factor.in/API/V1/ea498e73-cb38-11ee-8cbb-0200cd936042/SMS/{phn}/{photp}/OTP1'
    responseotp = requests.get(url)
    print(responseotp.status_code)
    if responseotp.status_code == 200:
        print("Yes OTP Successfully ")
    else:
        print("OTP is not Sent Due to Some Error ", responseotp.status_code)
























# Remaining views (table, edit, delete) remain unchanged



# def otpcheck(request):
#     if request.method == "POST":
#         mobile = request.session.get('mobile')
#         print("mobile->", mobile)
#         email = request.session.get('email')
#         user = Sgform.objects.filter(phn=mobile, eml=email)
#         print('email', user[0].eml)
#         otp1 = request.POST.get("otp1")
#         otp2 = request.POST.get("otp2")
#         otp3 = request.POST.get("otp3")
#         otp4 = request.POST.get("otp4")
#         print(otp1, otp2, otp3, otp4)
#         print(type('otp1'))
#         userotp = otp1 + otp2 + otp3 + otp4
#         print("User Otp is->", userotp)
#         print("Otp->", user[0].photp, type(user[0].photp))
#         if userotp == str(user[0].photp):
#             # otp1 = random.randint(1000, 9999)
#             # print('emailotp->', otp1)
#             # user[0].otp = str(otp1)
#             # user[0].save()  # Save the updated user object
#             # print('userotp->', user[0].photp, type(user[0].photp))
#             return redirect('otpcheck')
#         else:
#             # OTP is incorrect
#             print("Otp is incorrect !!!!!")
#             return redirect('otpcheck')
# #     # If request method is not POST, render the OTP verification page
#     return render(request, 'otp.html')
# #
# def form(request):
#     if request.method == "POST":
#         usn = request.POST.get("username")
#         phn = request.POST.get("phone")
#         eml = request.POST.get("email")
#         psd = request.POST.get("password")
#
#         # Generate OTP
#         emailotp = random.randint(1000, 9999)
#         print('emailotp->', emailotp)
#         request.session['email'] = eml
#         # print("email->",type(eml))
#         print(usn, phn, eml, psd, eml)
#         # Store email OTP in session
#         d ={'username': [usn],
#             'phone': [phn],
#             'email': [eml],
#             'password': [psd],
#             'emailotp': [emailotp]
#             }
#         df = pd.DataFrame(d)
#         df.to_csv('media/data.csv', index=False)
#         data = Sgform(usn=usn,
#                       phn=phn,
#                       eml=eml,
#                       psd=psd,
#                       # photp=photp,
#                       emailotp=emailotp)
#         data.save()
#         csv_file_path = "/media/data.csv"
#         csv_data = df.to_csv(index=False)
#         email = EmailMessage(
#             subject='CSV File Attached',
#             body='please find the csv file attached.',
#             from_email='settings.EMAIL_HOST_USER',
#             to=['prajal1305@gmail.com']
#         )
#         email.attach('data.csv', csv_data, 'text/CSV')
#
#         email.send()
#
#         return render(request, 'otp.html')
#
#     return render(request, 'form.html')
#
#
# def otpcheck(request):
#     email = request.session.get('email')
#     obj = Sgform.objects.filter(eml=email)
#     print("OTP is Verify status::=>", obj[0].emailotp, type(obj[0].emailotp), "email::=>", email)
#     if request.method == 'POST':
#         otp1 = request.POST.get('otp1')
#         otp2 = request.POST.get('otp2')
#         otp3 = request.POST.get('otp3')
#         otp4 = request.POST.get('otp4')
#
#         user_otp = otp1 + otp2 + otp3 + otp4
#         print("user_otp = ", user_otp)
#         print(type(user_otp))
#         # correct_otp = request.POST.get('otp')
#
#         if user_otp == obj[0].emailotp:
#         # Handle the case where OTP is correct
#             return redirect('dashboard')
#         else:
#             return render(request, 'otp.html', context={'error': "Invalid Data"})
#
#     return render(request, 'otp.html')
#

