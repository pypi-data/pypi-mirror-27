# Copyright (C) 2007-2017, Raffaele Salmaso <raffaele@salmaso.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from fluo.urls import reverse

from . import forms
from .models import TermsOfService, UserAgreement


class IndexView(View):
    def get(self, request):
        try:
            tos = TermsOfService.objects.current
        except TermsOfService.DoesNotExist:
            raise Http404
        return HttpResponseRedirect(reverse('legal-version', args=[tos.version]))


class TermsOfServiceView(View):
    def get(self, request, version):
        tos = get_object_or_404(TermsOfService, version=version)
        return render(request, 'legal/terms.html', {
            'tos': tos,
        })


class UserAgreementBaseView(View):
    form = forms.UserAgreementForm
    template_name = None
    message = None

    def initials(self, request, user, instance=None):
        initial = {}
        kwargs = {}
        tos = TermsOfService.objects.current
        try:
            ua = UserAgreement.objects.get(user=user, tos=tos.prev)
            for option in ua.options.all():
                kwargs[option.option.key] = option.value
        except TermsOfService.DoesNotExist:
            pass
        for option in tos.options.all():
            initial["tos_%s" % option.key] = kwargs.get(option.key, option.default)
        return initial

    def context(self, request, user):
        return {}

    def get_form(self, **kwargs):
        return self.form(**kwargs)

    def get(self, request):
        initial = self.initials(request, request.user)
        tos = TermsOfService.objects.current
        form = self.get_form(request=request, tos=tos, initial=initial)

        context = self.context(request, request.user)
        context.update({
            'form': form,
            'tos': tos,
            'complete': request.GET.get('complete', '') == 'true',
        })

        return render(request, self.template_name, context)

    def post(self, request):
        tos = TermsOfService.objects.current
        form = self.get_form(request=request, tos=tos, data=request.POST, files=request.FILES)
        if form.is_valid():
            instance = form.save(request=request)
            initial = self.initials(request, request.user, instance=instance)
            form = self.get_form(request=request, tos=tos, initial=initial)
            next = request.GET.get(REDIRECT_FIELD_NAME, None)
            if next:
                return HttpResponseRedirect(next)
            if self.message:
                messages.success(request, self.message)

        context = self.context(request, request.user)
        context.update({
            'form': form,
            'tos': tos,
            'complete': request.GET.get('complete', '') == 'true',
        })

        return render(request, self.template_name, context)
