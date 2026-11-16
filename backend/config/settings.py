from dotenv import load_dotenv
load_dotenv()
import os
from pathlib import Path
from datetime import timedelta
import dj_database_url
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-change-this-before-deploying")
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = [x.strip() for x in os.getenv("DJANGO_ALLOWED_HOSTS","localhost,127.0.0.1").split(",") if x.strip()]
INSTALLED_APPS = ["django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles","corsheaders","rest_framework","rest_framework_simplejwt","social"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware","whitenoise.middleware.WhiteNoiseMiddleware","corsheaders.middleware.CorsMiddleware","django.contrib.sessions.middleware.SessionMiddleware","django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware","django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF="config.urls"
TEMPLATES=[{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION="config.wsgi.application"
ASGI_APPLICATION="config.asgi.application"
DATABASES={"default":dj_database_url.config(default=os.getenv("DATABASE_URL",f"sqlite:///{BASE_DIR/'db.sqlite3'}"),conn_max_age=600)}
AUTH_USER_MODEL="social.User"
AUTH_PASSWORD_VALIDATORS=[{"NAME":"django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},{"NAME":"django.contrib.auth.password_validation.MinimumLengthValidator"},{"NAME":"django.contrib.auth.password_validation.CommonPasswordValidator"},{"NAME":"django.contrib.auth.password_validation.NumericPasswordValidator"}]
LANGUAGE_CODE="en-us"; TIME_ZONE="Asia/Kolkata"; USE_I18N=True; USE_TZ=True
STATIC_URL="static/"; STATIC_ROOT=BASE_DIR/"staticfiles"; STORAGES={"staticfiles":{"BACKEND":"whitenoise.storage.CompressedManifestStaticFilesStorage"}}; DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO","https")
if not DEBUG:
    SECURE_SSL_REDIRECT=os.getenv("SECURE_SSL_REDIRECT","True").lower()=="true"
    SESSION_COOKIE_SECURE=True
    CSRF_COOKIE_SECURE=True
EMAIL_BACKEND=os.getenv("EMAIL_BACKEND","django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL=os.getenv("DEFAULT_FROM_EMAIL","SnapSpace <no-reply@snapspace.local>")
EMAIL_HOST=os.getenv("EMAIL_HOST","")
EMAIL_PORT=int(os.getenv("EMAIL_PORT","587"))
EMAIL_HOST_USER=os.getenv("EMAIL_HOST_USER","")
EMAIL_HOST_PASSWORD=os.getenv("EMAIL_HOST_PASSWORD","")
EMAIL_USE_TLS=os.getenv("EMAIL_USE_TLS","True").lower()=="true"
EMAIL_USE_SSL=os.getenv("EMAIL_USE_SSL","False").lower()=="true"
CSRF_TRUSTED_ORIGINS=[x.strip() for x in os.getenv("CSRF_TRUSTED_ORIGINS","").split(",") if x.strip()]
CORS_ALLOWED_ORIGINS=[x.strip() for x in os.getenv("CORS_ALLOWED_ORIGINS","http://localhost:5000").split(",") if x.strip()]
REST_FRAMEWORK={"DEFAULT_AUTHENTICATION_CLASSES":["rest_framework_simplejwt.authentication.JWTAuthentication"],"DEFAULT_PERMISSION_CLASSES":["rest_framework.permissions.IsAuthenticated"],"DEFAULT_THROTTLE_CLASSES":["rest_framework.throttling.AnonRateThrottle","rest_framework.throttling.UserRateThrottle"],"DEFAULT_THROTTLE_RATES":{"anon":"30/minute","user":"120/minute"}}
SIMPLE_JWT={"ACCESS_TOKEN_LIFETIME":timedelta(minutes=15),"REFRESH_TOKEN_LIFETIME":timedelta(days=7),"ROTATE_REFRESH_TOKENS":True,"BLACKLIST_AFTER_ROTATION":True}
