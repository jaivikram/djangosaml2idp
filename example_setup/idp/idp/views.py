from django.conf import settings
from django.views.generic import TemplateView
from djangosaml2idp.models import ServiceProvider
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import resolve
from django.http import HttpResponseRedirect


class IndexView(TemplateView):
    template_name = "idp/redirect.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        url = reverse('djangosaml2idp:saml_idp_init')
        url += '?sp=http://192.168.56.101:8000/saml2/metadata/&RelayState='
        context.update({
            'url': url,
            'is_authenticated': self.request.user.is_authenticated,
            'user': self.request.user
        })
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.set_cookie(
            key='sessionid',
            value=request.session.session_key,
            domain="http://192.168.56.101:7000",
            max_age=1000
        )
        return response
    
    
# class IndexView(TemplateView):
        
#     def get(self, request, *args, **kwargs):
#         print(f"user: {request.user}")
#         url = reverse('djangosaml2idp:saml_idp_init')
#         url += '?sp=http://192.168.56.101:8000/saml2/metadata/&RelayState='
#         response = HttpResponseRedirect(url)
#         response.set_cookie(
#             key='sessionid',
#             value=request.session.session_key,
#             max_age=1000
#         )
#         print(request.session.session_key)
#         return request


class LinkoutView(TemplateView):
    template_name = "idp/index.html"

    def get_context_data(self, **kwargs):
        context = super(LinkoutView, self).get_context_data(**kwargs)
        context.update({
            "logout_url": settings.LOGOUT_URL,
            "login_url": settings.LOGIN_URL,
        })
        if self.request.user.is_authenticated:
            context.update({
                "user_attrs": sorted([(field.name, getattr(self.request.user, field.name)) for field in self.request.user._meta.get_fields() if field.concrete]),
                "known_sp_ids": [sp for sp in ServiceProvider.objects.filter(active=True)],
            })
        return context
