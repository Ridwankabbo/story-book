import os
from pathlib import Path
# from decouple import config
from datetime import timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$!@#^*&%^!@#*^&*!%$#@$^%!^@$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG =True

ALLOWED_HOSTS = [
    '*',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "https://alharasworld.com",
    "http://alharasworld.com",
    
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",    
    "http://alharasworld.com",
    "https://alharasworld.com",
]
CORS_ALLOW_ALL_ORIGINS = True
# Application definition

INSTALLED_APPS = [
    # django unfold theme 
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "unfold.contrib.location_field",
    # default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'drf_yasg',
    # lcoal
    'apps.account',
    'apps.guardians',
    'apps.products',
    'apps.videos',
    'apps.quiz',
    'apps.forms',
    'apps.template_info'

]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 3rd party middleware

    # custom middleware
    "drf_response_wrapper.middleware.APIResponseWrapperMiddleware",
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # custom context processors
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# for asgi
# ASGI_APPLICATION = 'project.asgi.application'



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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


###################################
#             DATABASE            #
###################################
from .conf import database
DATABASES = database.SQLITE


# CONSOLE EMAIL BACKEND
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # use in development only

#################### SMTP EMAIL BACKEND ######################
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = config('EMAIL_HOST', default='localhost')
# EMAIL_PORT = config('EMAIL_PORT', default=25)
# EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
# EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'sifatali360@gmail.com'
EMAIL_HOST_PASSWORD = 'huhe rrbm klcz nfdv'

###################################
#         STATIC FILES            #
###################################

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR/'static',
]
STATIC_ROOT = BASE_DIR/'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR/'media'

# Default file storage
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

###################################
#                DRF              #
###################################

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.account.authentication.BlacklistAwareJWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'EXCEPTION_HANDLER': 'project.custom_exception.custom_exception_handler',
}

SWAGGER_SETTINGS = {
    'DEFAULT_INFO': 'project.urls.api_info',
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=200),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=300),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
}

# Custom User Model
AUTH_USER_MODEL = 'account.User'



STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
FRONTEND_SUCCESS_URL = "https://alharasworld.com/profile/my-orders"
FRONTEND_CANCEL_URL = "https://alharasworld.com/payment-error/"

from django.templatetags.static import static
from django.urls import reverse_lazy, reverse, NoReverseMatch
from django.utils.translation import gettext_lazy as _

# helper to safely reverse named urls that may not be registered
def _safe_reverse(name):
    try:
        return reverse(name)
    except NoReverseMatch:
        return "#"

# helper to pick an icon name based on a title/name string
def _icon_for_title(title):
    t = str(title).lower()
    # Material (Google) icon names
    mapping = {
        'user': 'group',
        'book': 'menu_book',
        'books': 'menu_book',
        'product': 'inventory',
        'attribute': 'badge',
        'order': 'receipt_long',
        'status': 'alt_route',
        'cart': 'shopping_cart',
        'guardian': 'security',
        'quiz': 'quiz',
        'video': 'videocam',
        'poll': 'poll',
        'newsletter': 'mail',
        'kit': 'extension',
        'gallery': 'collections',
        'galleries': 'collections',
        'classroom': 'school',
        'partnership': 'business',
    }
    for k, v in mapping.items():
        if k in t:
            return v
    return 'help_outline'

UNFOLD = {
    "SITE_TITLE": "AL HARAS Admin",  # appears in browser title bar
    "SITE_HEADER": "AL HARAS Admin",
    "SITE_SUBHEADER": "ALL YOU NEED IN ONE PLACE",
    "DASHBOARD_CALLBACK": "apps.videos.views.dashboard_callback",

    "SITE_URL": "/",
    "SITE_SYMBOL": "automation",  # symbol from icon set
    "SHOW_THEME_SWITCHER": False,
    "THEME": "light",

    "SHOW_HISTORY": True, # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True, # show/hide "View on site" button, default: True
    "SHOW_BACK_BUTTON": False, # show/hide "Back" button on changeform in header, default: False
    "SHOW_THEME_SWITCHER": False,  # disable theme switcher
    # "THEME": "light", # Force light theme
    
    "STYLES": [
        lambda request: static("css/style.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/script.js"),
    ],

    
    "SIDEBAR": {
        "show_search": False,  # Search in applications and models names
        "command_search": False,  # Replace the sidebar search with the command search
        "show_all_applications": False,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("User Management"),
                "separator": True,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [
                    {
                        "title": _("User"),
                        "icon": _icon_for_title("User"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:account_user_changelist"),
                        "badge_variant": "info", # info, success, warning, primary, danger
                        "badge_style": "solid", # background fill style
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("Product Management"),
                "separator": True,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Books Manage"),
                        "icon": _icon_for_title("Books Manage"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:products_books_changelist"),
                        "badge_variant": "info", # info, success, warning, primary, danger
                        "badge_style": "solid", # background fill style
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Mission Galleries"),
                        "icon": _icon_for_title("Mission Galleries"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:products_missiongallery_changelist"),
                        "badge_variant": "info",
                        "badge_style": "solid",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Product Manage"),
                        "icon": _icon_for_title("Product Manage"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:products_product_changelist"),
                        "badge_variant": "info", # info, success, warning, primary, danger
                        "badge_style": "solid", # background fill style
                        "permission": lambda request: request.user.is_superuser,
                    },
                    # {
                    #     "title": _("Product Attributes"),
                    #     "icon": _icon_for_title("Product Attributes"),  # Supported icon set: https://fonts.google.com/icons
                    #     "link": lambda request: _safe_reverse("admin:products_productattribute_changelist"),
                    #     "badge_variant": "info", # info, success, warning, primary, danger
                    #     "badge_style": "solid", # background fill style
                    #     "permission": lambda request: request.user.is_superuser,
                    # },
                ],
            },
            {
                "title": _("Orders Management"),
                "separator": True,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Orders Manage"),
                        "icon": _icon_for_title("Orders Manage"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:products_order_changelist"),
                        "badge_variant": "info", # info, success, warning, primary, danger
                        "badge_style": "solid", # background fill style
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Order Status Logs"),
                        "icon": _icon_for_title("Order Status Logs"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:products_orderstatuslog_changelist"),
                        "badge_variant": "info", # info, success, warning, primary, danger
                        "badge_style": "solid", # background fill style
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("User Carts"),
                "separator": True,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Carts"),
                        "icon": _icon_for_title("Carts"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:products_cart_changelist"),
                        "badge_variant": "info", # info, success, warning, primary, danger
                        "badge_style": "solid", # background fill style
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Cart Items"),
                        "icon": _icon_for_title("Cart Items"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:products_cartitem_changelist"),
                        "badge_variant": "info", # info, success, warning, primary, danger
                        "badge_style": "solid", # background fill style
                        "permission": lambda request: request.user.is_superuser,
                    },
                    
                ],
            },
            {
                "title": _("Guardian Management"),
                "separator": True,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Guardian Manage"),
                        "icon": _icon_for_title("Guardian Manage"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:guardians_guardian_changelist"),
                        "badge_variant": "info", # info, success, warning, primary, danger
                        "badge_style": "solid", # background fill style
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Country Manage"),
                        "icon": _icon_for_title("Country Manage"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:guardians_country_changelist"),
                        "badge_variant": "info", # info, success, warning, primary, danger
                        "badge_style": "solid", # background fill style
                        "permission": lambda request: request.user.is_superuser,
                    },
                    
                ],
            },
            {
                "title": _("Quiz Management"),
                "separator": True,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Quiz Set Manage"),
                        "icon": _icon_for_title("Quiz Set Manage"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:quiz_quizset_changelist"),
                        "badge_variant": "info", # info, success, warning, primary, danger
                        "badge_style": "solid", # background fill style
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Quiz Questions Manage"),
                        "icon": _icon_for_title("Quiz Questions Manage"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:quiz_question_changelist"),
                        "badge_variant": "info", # info, success, warning, primary, danger
                        "badge_style": "solid", # background fill style
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Quiz Options Manage"),
                        "icon": _icon_for_title("Quiz Options Manage"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:quiz_option_changelist"),
                        "badge_variant": "info", # info, success, warning, primary, danger
                        "badge_style": "solid", # background fill style
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Quiz Attempts Data"),
                        "icon": _icon_for_title("Quiz Attempts Data"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:quiz_quizattempt_changelist"),
                        "badge_variant": "info", # info, success, warning, primary, danger
                        "badge_style": "solid", # background fill style
                        "permission": lambda request: request.user.is_superuser,
                    },
                    
                ],
            },
            {
                "title": _("Video Management"),
                "separator": True,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Video Manage"),
                        "icon": _icon_for_title("Video Manage"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:videos_video_changelist"),
                        "badge_variant": "info", # info, success, warning, primary, danger
                        "badge_style": "solid", # background fill style
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Mini Game Backgrounds"),
                        "icon": _icon_for_title("Mini Game Backgrounds"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:videos_minigamebakgroudn_changelist"),
                        "badge_variant": "info", # info, success, warning, primary, danger
                        "badge_style": "solid", # background fill style
                        "permission": lambda request: request.user.is_superuser,
                    },
                    
                ],
            },
            {
                "title": _("Classroom Data"),
                "separator": True,  # Top border
                "collapsible": False,
                "items": [
                    {
                        "title": _("Classroom Data"),
                        "icon": _icon_for_title("Classroom Data"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:videos_classroomdata_changelist"),
                        "badge_variant": "info",
                        "badge_style": "solid",
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("Poll Management"),
                "separator": True,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Poll Manage"),
                        "icon": _icon_for_title("Poll Manage"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:videos_poll_changelist"),
                        "badge_variant": "info", # info, success, warning, primary, danger
                        "badge_style": "solid", # background fill style
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Poll Options"),
                        "icon": _icon_for_title("Poll Options"),  # Supported icon set: https://fonts.google.com/icons
                        "link": lambda request: _safe_reverse("admin:videos_polloption_changelist"),
                        "badge_variant": "info", # info, success, warning, primary, danger
                        "badge_style": "solid", # background fill style
                        "permission": lambda request: request.user.is_superuser,
                    },
                    # {
                    #     "title": _("Poll Votes"),
                    #     "icon": _icon_for_title("Poll Votes"),  # Supported icon set: https://fonts.google.com/icons
                    #     "link": lambda request: _safe_reverse("admin:videos_pollvote_changelist"),
                    #     "badge_variant": "info", # info, success, warning, primary, danger
                    #     "badge_style": "solid", # background fill style
                    #     "permission": lambda request: request.user.is_superuser,
                    # },
                    
                ],
            },
            {
                "title": _("Kit and Forms Management"),
                "separator": True,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Newsletter Subscribed"),
                        "icon": _icon_for_title("Newsletter Subscribed"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:forms_newslettersubscription_changelist"),
                        "badge_variant": "info", # info, success, warning, primary, danger
                        "badge_style": "solid", # background fill style
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("KIT Requests"),
                        "icon": _icon_for_title("KIT Requests"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:forms_alherakitrequest_changelist"),
                        "badge_variant": "info", # info, success, warning, primary, danger
                        "badge_style": "solid", # background fill style
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Partnership Inquiries"),
                        "icon": _icon_for_title("Partnership Inquiries"),  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:forms_partnershipinquary_changelist"),
                        "badge_variant": "info", # info, success, warning, primary, danger
                        "badge_style": "solid", # background fill style
                        "permission": lambda request: request.user.is_superuser,
                    },
                    
                ],
            },
            {
                "title": _("Template Content"),
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": _("Page Content"),
                        "icon": _icon_for_title("Page Content"),
                        "link": reverse_lazy("admin:template_info_pagecontent_changelist"),
                        "badge_variant": "info",
                        "badge_style": "solid",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Vehicles Categories"),
                        "icon": _icon_for_title("Vehicle Categories"),
                        "link": reverse_lazy("admin:template_info_vehiclescategory_changelist"),
                        "badge_variant": "info",
                        "badge_style": "solid",
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            
        ],
    },
}
