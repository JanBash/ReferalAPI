from django.core.mail import send_mail
from .models import *
import requests
from datetime import date

def send_email(receiver, pk):
    try:
        subject = 'It is test govno'
        refer_obj = Refer.objects.filter(user = pk).filter(expire_date__gt = date.today()).first()
        message = f'Refer code --> {refer_obj.code}' 
        send_mail(subject, message, 'sakirovzanbolot48@gmail.com', receiver)
    except:
        raise 

def check_email_existence(email):
    url = f'https://api.hunter.io/v2/email-verifier?email={email}&api_key=0fff49789882a99e01552503036c8fa757680b81'

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
    