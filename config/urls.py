from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from django.views import defaults as default_views
from django.contrib.auth import views as auth_views

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls
from cosme.v1.views import (
    ExternalURLNoticeView,
    login_with_lockout,
    check_permissions,
    welcome,
    change_password,
    CustomPasswordResetConfirmView,
)
from cosme.v1.forms import COSMEPasswordChangeForm

urlpatterns = [
    # path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    # path(
    #     "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    # ),
    re_path(
        r"^home/(?P<path>.*)$", RedirectView.as_view(url="/%(path)s", permanent=True)
    ),
    # # Django Admin, use {% url 'admin:index' %}
    # path(settings.ADMIN_URL, admin.site.urls),
    # User management
    # path("users/", include("cosme.users.urls", namespace="users")),
    # path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    # re_path(r"^admin/", include(wagtailadmin_urls)),
    re_path(r"^documents/", include(wagtaildocs_urls)),
    re_path(r"^pages/", include(wagtail_urls)),
    re_path(r"^external-site/$", ExternalURLNoticeView.as_view(), name="external-site"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.ALLOW_ADMIN_URL:
    patterns = [
        re_path(r"^login/$", login_with_lockout, name="cfpb_login"),
        re_path(
            r"^login/check_permissions/$", check_permissions, name="check_permissions"
        ),
        re_path(r"^login/welcome/$", welcome, name="welcome"),
        re_path(r"^logout/$", auth_views.logout),
        re_path(
            "^admin/login/$",
            RedirectView.as_view(url="/login/", permanent=True, query_string=True),
        ),
        re_path(
            "^django-admin/login/$",
            RedirectView.as_view(url="/login/", permanent=True, query_string=True),
        ),
        re_path(
            r"^d/admin/(?P<path>.*)$",
            RedirectView.as_view(url="/django-admin/%(path)s", permanent=True),
        ),
        re_path(
            r"^tasks/(?P<path>.*)$",
            RedirectView.as_view(url="/admin/cdn/%(path)s", permanent=True),
        ),
        re_path(
            r"^django-admin/password_change",
            change_password,
            name="django_admin_account_change_password",
        ),
        re_path(r"^django-admin/", admin.site.urls),
        # Override Django and Wagtail password views with our password policy
        re_path(
            r"^admin/password_reset/",
            include(
                [
                    re_path(
                        r"^confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
                        # noqa: E501
                        CustomPasswordResetConfirmView.as_view(),
                        name="password_reset_confirm",
                    )
                ]
            ),
        ),
        re_path(
            r"^django-admin/password_change",
            auth_views.password_change,
            {"password_change_form": COSMEPasswordChangeForm},
        ),
        re_path(
            r"^password/change/done/$",
            auth_views.password_change_done,
            name="password_change_done",
        ),
        re_path(
            r"^admin/account/change_password/$",
            change_password,
            name="wagtailadmin_account_change_password",
        ),
        re_path(r"^admin/", include(wagtailadmin_urls)),
    ]

    urlpatterns = patterns + urlpatterns

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
