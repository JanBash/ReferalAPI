from django.core.mail import send_mail
from .models import *
import requests
from datetime import date

# Function to send email
def send_email(receiver, pk):
    try:
        subject = "You'r referal code"
        refer_obj = Refer.objects.filter(user = pk).filter(expire_date__gt = date.today()).first()
        message = f'Referal code --> {refer_obj.code}' 
        send_mail(subject, message, 'sakirovzanbolot48@gmail.com', receiver) # Change email to whatever email you want --> 'email@example.com'
    except:
        raise 

# function for emailhunter API
def check_email_existence(email):
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key='write_you'r_own_key_here'"

    response = requests.get(url)
    data = response.json()
    print(data)

    if 'data' in data:
        if data['data']['status'] == 'valid' or data['data']['status'] == 'accept_all':
            if data['data']['result'] == 'deliverable' or data['data']['result'] == 'risky':
                return True
        elif data['data']['status'] == 'invalid':
            return False
        else:
            # Обработка ошибки
            return False
    elif 'data' not in data:
        return False
    
