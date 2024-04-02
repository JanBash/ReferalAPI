# Referal API

## Description

This simple Python DRF application was created to learn about SMTP. In this file, I will explain how to run this project and use SMTP, as well as a third-party API for email existence checking.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

To start clone this repository:

    git clone https://github.com/JanBash/ReferalAPI.git

Now you need to install [Django Rest Framework](https://www.django-rest-framework.org) and [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html) 

## Usage

To start using this project you need to get from Google your app password, you can get this in your account settings, just search 'app password'

Once you get it you need to write it in settings.py

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST_USER = '' # <-- email here
    EMAIL_HOST_PASSWORD = '' # <-- Code from Google

Then you need to go to [emailhunter](https://hunter.io), here you need to log in and take API for email verification that looks like this:

    https://api.hunter.io/v2/email-verifier?email=patrick@stripe.com&api_key=[your_special_key]

Put that url in check_email_existance function in utils.py like this

    def check_email_existence(email):
        url = f"https://api.hunter.io/v2/email-verifier?email=patrick@stripe.com&api_key=[your_special_key]"

Then you finally can run the project

First, create the superuser, to create superuser you need to type in terminal where the manage.py located:

    $ python manage.py createsuperuser

or

    $ python3 manage.py createsuperuser

then just to make sure apply migrations by typing:

    $ python manage.py make migrations
    $ python manege.py migrate

then you can run server:

    $ python manage.py runserver

## Contributing

Maybe you can face the problems with check_email_existence function

    def check_email_existence(email):
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key='write_you'r_own_key_here'"

    response = requests.get(url)
    data = response.json()
    print(data['data'])

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

Because here we validate the response wit data['data']['status'], just write print(data['data']) before 'if' to check the response.

## License

### This is my first Readme file, I hope this was informative for you.
