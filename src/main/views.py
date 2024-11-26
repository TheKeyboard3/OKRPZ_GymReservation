from django.http import HttpRequest, Http404
from django.shortcuts import render
from django.views import View
from core.settings.base import SITE_SUPPORT_EMAIL


class IndexView(View):

    def get(self, request: HttpRequest):
        return render(request, 'main/index.html')


class AboutView(View):

    def get(self, request: HttpRequest):
        context = {
            'support_email': SITE_SUPPORT_EMAIL,
        }
        return render(request, 'main/about.html', context)


class NotFoundView(View):

    def get(self, request: HttpRequest):
        raise Http404()
