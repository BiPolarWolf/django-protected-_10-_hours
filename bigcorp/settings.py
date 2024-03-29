
from pathlib import Path
from django.conf.global_settings import STATICFILES_DIRS, STATICFILES_FINDERS
from dotenv import load_dotenv ,dotenv_values
import dotenv


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = dotenv_values('.env').get('SECRET_KEY')

DEBUG = bool(int(dotenv_values('.env').get('DEBUG')))

ALLOWED_HOSTS = ['*']

load_dotenv()


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',

    #email verification
    'django_email_verification',

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #3rd party libs
    'mathfilters',
    'crispy_forms',
    "crispy_bootstrap5",
    'django_google_fonts',

    #apps
    'shop.apps.ShopConfig',
    'cart.apps.CartConfig',
    'account.apps.AccountConfig',
    'payment.apps.PaymentConfig',
    
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bigcorp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'bigcorp' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                #custom context processors
                'shop.context_processors.categories',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'bigcorp.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


#Project inside settings

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Aqtobe'

USE_I18N = True

USE_TZ = True


# static files

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = BASE_DIR / 'bigcorp' / 'static',

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'



#fonts

GOOGLE_FONTS = ["Montserrat:wght@300,400", "Roboto"]
GOOGLE_FONTS_DIR = BASE_DIR / "static"

#crispy forms

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


#Email Verification settings

def email_verified_callback(user):
    user.is_active = True


def password_change_callback(user, password):
    user.set_password(password)



# Global Package Settings
EMAIL_FROM_ADDRESS = 'snegirgik@gmail.com'  # mandatory
EMAIL_PAGE_DOMAIN = 'http://127.0.0.1:8000/'  # mandatory (unless you use a custom link)
EMAIL_MULTI_USER = False  # optional (defaults to False)

# Email Verification Settings (mandatory for email sending)
EMAIL_MAIL_SUBJECT = 'Confirm your email {{ user.username }}'
EMAIL_MAIL_HTML = 'account/email/mail_body.html'
EMAIL_MAIL_PLAIN = 'account/email/mail_body.txt'
EMAIL_MAIL_TOKEN_LIFE = 60 * 60  # one hour

# Email Verification Settings (mandatory for builtin view)
EMAIL_MAIL_PAGE_TEMPLATE = 'account/email/email_success_template.html'
EMAIL_MAIL_CALLBACK = email_verified_callback

# Password Recovery Settings (mandatory for email sending)
EMAIL_PASSWORD_SUBJECT = 'Change your password {{ user.username }}'
EMAIL_PASSWORD_HTML = 'password_body.html'
EMAIL_PASSWORD_PLAIN = 'password_body.txt'
EMAIL_PASSWORD_TOKEN_LIFE = 60 * 10  # 10 minutes

# Password Recovery Settings (mandatory for builtin view)
EMAIL_PASSWORD_PAGE_TEMPLATE = 'password_changed_template.html'
EMAIL_PASSWORD_CHANGE_PAGE_TEMPLATE = 'password_change_template.html'
EMAIL_PASSWORD_CALLBACK = password_change_callback

# For Django Email Backend
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'snegirgik@gmail.com'
EMAIL_HOST_PASSWORD =  dotenv_values('.env')['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = True


#stripe

STRIPE_PUBLISHED_KEY = dotenv_values('.env')['STRIPE_PUBLISHED_KEY']
STRIPE_SECRET_KEY = dotenv_values('.env')['STRIPE_SECRET_KEY']
STRIPE_API_VERSION = '2020-08-27'

#Yookassa

YOOKASSA_SECRET_KEY = dotenv_values('.env')['YOOKASSA_SECRET_KEY']
YOOKASSA_SHOP_ID = dotenv_values('.env')['YOOKASSA_SHOP_ID']
