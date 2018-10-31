from django.http import Http404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin

from cosme.v1.forms import ExternalURLForm


class ExternalURLNoticeView(FormMixin, TemplateView):
    template_name = 'external-site/index.html'
    form_class = ExternalURLForm

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ExternalURLNoticeView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ExternalURLNoticeView, self).get_form_kwargs()

        if self.request.method == 'GET':
            kwargs['data'] = self.request.GET

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ExternalURLNoticeView, self).get_context_data(**kwargs)

        form = self.get_form()
        context['form'] = form

        return context

    def get(self, request, *args, **kwargs):
        form = self.get_form()

        if not form.is_valid():
            return self.raise_404()

        return super(ExternalURLNoticeView, self).get(request)

    def post(self, request):
        form = self.get_form()

        if not form.is_valid():
            return self.raise_404()

        return redirect(form.cleaned_data['validated_url'])

    def raise_404(self):
        raise Http404(
            'URL invalid, not whitelisted, or signature validation failed'
        )
