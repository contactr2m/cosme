from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    REDIRECT_FIELD_NAME,
    get_user_model,
    login as auth_login,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.urls import resolve, reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render, resolve_url
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import views as auth_views
from django.utils.decorators import method_decorator
from wagtail.admin.views import account
from wagtail.admin.views.account import PasswordResetConfirmView

from ..forms import COSMEPasswordChangeForm, COSMESetPasswordForm, LoginForm
from ..util.util import all_valid_destinations_for_request


# Overrided Wagtail Views
@login_required
def change_password(request):
    if not account.password_management_enabled():
        raise Http404

    user = request.user
    can_change_password = user.has_usable_password()

    if not can_change_password:
        form = None

    if request.POST:
        form = COSMEPasswordChangeForm(user=user, data=request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)

            messages.success(request, _("Your password has been changed successfully!"))
            return redirect("wagtailadmin_account")
        else:
            if "__all__" in form.errors:
                for error in form.errors["__all__"]:
                    messages.error(request, error)
    else:
        form = COSMEPasswordChangeForm(user=request.user)

    return render(
        request,
        "wagtailadmin/account/change_password.html",
        {"form": form, "can_change_password": can_change_password},
    )


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login_with_lockout(request, template_name="wagtailadmin/login.html"):
    """
	Displays the login form and handles the login action.
	"""
    redirect_to = request.POST.get(
        REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME, "")
    )

    # Redirects to https://example.com should not be allowed.
    if redirect_to:
        if "//" in redirect_to:
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            user = form.get_user()
            try:
                user.failedloginattempt.delete()
            except ObjectDoesNotExist:
                pass

            auth_login(request, form.get_user())

            return HttpResponseRedirect("/login/check_permissions/?next=" + redirect_to)
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect("/login/check_permissions/?next=" + redirect_to)
        form = LoginForm(request)

    current_site = get_current_site(request)

    context = {
        "form": form,
        REDIRECT_FIELD_NAME: redirect_to,
        "site": current_site,
        "site_name": current_site.name,
    }

    context.update(
        {
            "show_password_reset": account.password_reset_enabled(),
            "username_field": get_user_model().USERNAME_FIELD,
        }
    )

    return TemplateResponse(request, template_name, context)


@never_cache
def check_permissions(request):
    redirect_to = request.POST.get(
        REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME, "")
    )

    if not request.user.is_authenticated:
        return HttpResponseRedirect(
            "%s?%s=%s" % (settings.LOGIN_URL, REDIRECT_FIELD_NAME, redirect_to)
        )
    view, args, kwargs = resolve(redirect_to)
    kwargs["request"] = request
    try:
        response = view(*args, **kwargs)
    except (Http404, TypeError):
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    if isinstance(response, HttpResponseRedirect):
        # this indicates a permissions problem
        # (there may be a better way)
        if REDIRECT_FIELD_NAME + "=" in response.url:
            return render(
                request,
                "wagtailadmin/access_denied.html",
                context={
                    "attempted_to_reach": redirect_to,
                    "destinations": all_valid_destinations_for_request(request),
                },
            )

    return HttpResponseRedirect(redirect_to)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = COSMESetPasswordForm
    template_name = "wagtailadmin/account/password_reset/confirm.html"
    success_url = reverse_lazy("wagtailadmin_password_reset_complete")

    def form_valid(self, form):
        user = form.save()
        user.temporarylockout_set.all().delete()
        del self.request.session[auth_views.INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)


@never_cache
@login_required
def welcome(request):
    valid_destinations = all_valid_destinations_for_request(request)

    if len(valid_destinations) == 1:
        redirect_to = valid_destinations[0][1]
        return HttpResponseRedirect(redirect_to)

    else:
        return render(request, "welcome.html", {"destinations": valid_destinations})
