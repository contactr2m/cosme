"""
Base settings to build other settings files upon.
"""

import environ
import os

# (cosme/config/settings/base.py - 3 = cosme/)
ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path("cosme")
V1_TEMPLATE_ROOT = APPS_DIR.path("jinja2/v1/")

env = environ.Env()

# Deploy environment
DEPLOY_ENVIRONMENT = os.getenv("DEPLOY_ENVIRONMENT", "beta")

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR.path(".env")))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
ALLOW_ADMIN_URL = env.bool("ALLOW_ADMIN_URL", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "EST"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {"default": env.db("DATABASE_URL", default="postgres:///cosme")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 'django.contrib.humanize', # Handy template tags
    "django.contrib.admin",
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_framework",
    "flags",
    "wagtailflags",
    # "overextends",
]
WAGTAIL_APPS = [
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    "modelcluster",
    "taggit",
]
LOCAL_APPS = [
    "cosme.users.apps.UsersAppConfig",
    "wagtailinventory",
    "cosme.v1",
    "storages",
    # Your stuff: custom apps go here
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS + WAGTAIL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "cosme.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
# LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
# LOGIN_URL = "account_login"
LOGIN_FAIL_TIME_PERIOD = os.environ.get("LOGIN_FAIL_TIME_PERIOD", 120 * 60)
# number of failed attempts
LOGIN_FAILS_ALLOWED = os.environ.get("LOGIN_FAILS_ALLOWED", 5)
LOGIN_REDIRECT_URL = "/login/welcome/"
LOGIN_URL = "/login/"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.core.middleware.SiteMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "cosme.v1.middleware.ParseLinksMiddleware",
    "cosme.v1.middleware.DownstreamCacheControlMiddleware",
    "flags.middleware.FlagConditionsMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR("staticfiles"))
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path("static")),
    str(APPS_DIR.path("templates/wagtailadmin")),
]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR("media"))
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
# We support two different template engines: Django & Jinja2 templates.
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(APPS_DIR.path("templates"))],
        # Look for Django templates in each app under a templates subdirectory.
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            "debug": DEBUG,
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            # "loaders": [
            #     "django.template.loaders.filesystem.Loader",
            #     "django.template.loaders.app_directories.Loader",
            # ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
            # "builtins": ["overextends.templatetags.overextends_tags"],
        },
    },
    {
        "NAME": "wagtail-env",
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        # Look for Jinja2 templates in these directories.
        "DIRS": [
            V1_TEMPLATE_ROOT,
            V1_TEMPLATE_ROOT.path("_includes"),
            V1_TEMPLATE_ROOT.path("_layouts"),
        ],
        # Look for Jinja2 templates in each app under a jinja2 subdirectory.
        "APP_DIRS": True,
        "OPTIONS": {
            "environment": "cosme.v1.jinja2_environment.environment",
            "extensions": [
                "jinja2.ext.do",
                "jinja2.ext.i18n",
                "jinja2.ext.loopcontrols",
                "wagtail.core.jinja2tags.core",
                "wagtail.admin.jinja2tags.userbar",
                "wagtail.images.jinja2tags.images",
                "cosme.v1.jinja2tags.core_extension.filters",
                "cosme.v1.jinja2tags.datetimes_extension",
                "cosme.v1.jinja2tags.fragment_cache_extension",
                "cosme.v1.jinja2tags.v1_extension",
            ],
        },
    },
]
# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap4"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Rohit""", "rohit@example.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "username"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = "cosme.users.adapters.AccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = "cosme.users.adapters.SocialAccountAdapter"

# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation
INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]
# Your stuff...
# ------------------------------------------------------------------------------

WAGTAIL_SITE_NAME = "COSME"
WAGTAILIMAGES_IMAGE_MODEL = "v1.COSMEImage"
TAGGIT_CASE_INSENSITIVE = True

# We want the ability to serve the latest drafts of some pages on beta.
# This value is read by v1.wagtail_hooks.
SERVE_LATEST_DRAFT_PAGES = []

# To expose a previously-published page's latest draft version on beta,
# add its primary key to the list below.
if DEPLOY_ENVIRONMENT == "beta":
    SERVE_LATEST_DRAFT_PAGES = []

# Feature flags
# All feature flags must be listed here with a dict of any hard-coded
# conditions or an empty dict. If the conditions dict is empty the flag will
# only be enabled if database conditions are added.
FLAGS = {
    # Ask COSME search spelling correction support
    # When enabled, spelling suggestions will appear in Ask COSME search and
    # will be used when the given search term provides no results.
    "ASK_SEARCH_TYPOS": {},
    # Beta banner, seen on beta.cosme.in
    # When enabled, a banner appears across the top of the site proclaiming
    # "This beta site is a work in progress."
    "BETA_NOTICE": {"environment_is": "beta"},
    # "BETA_NOTICE": {"boolean": False},
    # When enabled, include a recruitment code comment in the base template.
    "CFPB_RECRUITING": {},
    # When enabled, display a "technical issues" banner on /complaintdatabase.
    "CCDB_TECHNICAL_ISSUES": {},
    # When enabled, use Wagtail for /company-signup/ (instead of selfregistration app)
    "WAGTAIL_COMPANY_SIGNUP": {},
    # To be enabled when mortgage-performance data visualizations go live
    "MORTGAGE_PERFORMANCE_RELEASE": {},
    # Google Optimize code snippets for A/B testing
    # When enabled this flag will add various Google Optimize code snippets.
    # Intended for use with path conditions.
    "AB_TESTING": {},
    # Email popups.
    "EMAIL_POPUP_OAH": {"boolean": True},
    "EMAIL_POPUP_DEBT": {"boolean": True},
    # Wagtail menu
    "WAGTAIL_MENU": {},
    # The release of new Whistleblowers content/pages
    "WHISTLEBLOWER_RELEASE": {},
    # Turbolinks is a JS library that speeds up page loads
    # https://github.com/turbolinks/turbolinks
    "TURBOLINKS": {},
    # Ping google on page publication in production only
    "PING_GOOGLE_ON_PUBLISH": {"environment_is": "production"},
    "BCFP_LOGO": {},
}

EMAIL_POPUP_URLS = {
    "debt": [
        "/ask-cfpb/what-is-a-statute-of-limitations-on-a-debt-en-1389/",
        "/ask-cfpb/what-is-the-best-way-to-negotiate-a-settlement-with-a-debt-collector-en-1447/",
        "/ask-cfpb/what-should-i-do-when-a-debt-collector-contacts-me-en-1695/",
        "/consumer-tools/debt-collection/",
    ],
    "oah": ["/owning-a-home/", "/owning-a-home/mortgage-estimate/"],
}

# Optionally enable cache for general template fragments
if os.environ.get("ENABLE_DEFAULT_FRAGMENT_CACHE"):
    CACHES = {
        "default_fragment_cache": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": "default_fragment_cache",
            "TIMEOUT": None,
        }
    }
else:
    CACHES = {
        "default_fragment_cache": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
            "TIMEOUT": 0,
        }
    }

# WAGTAIL_APPEND_SLASH = False

PARSE_LINKS_BLACKLIST = ["/admin/", "/django-admin/"]

