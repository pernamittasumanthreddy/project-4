"""
Django settings for HMS Enterprise Multi-Tenant SaaS Platform.
Member 7: Portals, Telemedicine, Notifications, QA, CI/CD and Cross-Module Integration.
"""

from pathlib import Path
import os
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / 'apps'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-hms-saas-enterprise-member7-core-key-2026-prod-grade')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party dependencies
    'rest_framework',
    'corsheaders',
    'django_filters',
    'drf_spectacular',

    # HMS Core Architecture Modules
    'apps.core.apps.CoreConfig',
    'apps.appointments.apps.AppointmentsConfig',
    'apps.clinical.apps.ClinicalConfig',
    'apps.diagnostics.apps.DiagnosticsConfig',
    'apps.pharmacy.apps.PharmacyConfig',
    'apps.billing.apps.BillingConfig',

    # Member 7 Primary Modules
    'apps.notifications.apps.NotificationsConfig',
    'apps.telemedicine.apps.TelemedicineConfig',
    'apps.patient_portal.apps.PatientPortalConfig',
    'apps.doctor_portal.apps.DoctorPortalConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'apps.core.middleware.TenantContextMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hms_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hms_core.wsgi.application'
ASGI_APPLICATION = 'hms_core.asgi.application'

# Database configuration: Default local zero-config SQLite with PostgreSQL compatibility
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'hms_enterprise.sqlite3',
    }
}

# Custom User Model
AUTH_USER_MODEL = 'core.User'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 6},
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.core.authentication.DemonstrationSessionAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'EXCEPTION_HANDLER': 'apps.core.exceptions.custom_exception_handler',
}

# CORS settings for Frontend React client
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-tenant-id',
    'x-impersonate-user',
]

# Notification Engine Settings (Zero external paid API keys)
NOTIFICATION_SETTINGS = {
    'EMAIL_BACKEND': 'apps.notifications.adapters.ConsoleEmailAdapter',
    'SMS_BACKEND': 'apps.notifications.adapters.ConsoleSMSAdapter',
    'DEFAULT_FROM_EMAIL': 'no-reply@hms-saas.health',
    'RETRY_MAX_ATTEMPTS': 3,
    'LOG_FILE': BASE_DIR / 'notifications_delivery.log',
}

# Telemedicine WebRTC Configuration (Public STUN fallback, zero paid credentials)
TELEMEDICINE_SETTINGS = {
    'ICE_SERVERS': [
        {'urls': ['stun:stun.l.google.com:19302', 'stun:stun1.l.google.com:19302']},
    ],
    'SESSION_EXPIRY_MINUTES': 90,
    'ALLOW_RECORDING': False,
    'WAITING_ROOM_TIMEOUT_SECONDS': 1800,
}
