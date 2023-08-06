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

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from fluo import admin, forms

from .models import (
    Option, OptionTranslation, TermsOfService, TermsOfServiceTranslation, UserAgreement, UserAgreementOption,
)

LANG = len(settings.LANGUAGES)


class OptionTranslationInlineForm(forms.ModelForm):
    pass


class OptionTranslationInline(admin.StackedInline):
    form = OptionTranslationInlineForm
    model = OptionTranslation
    extra = 0
    max_num = LANG


class OptionAdminForm(forms.ModelForm):
    pass


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    form = OptionAdminForm
    inlines = (OptionTranslationInline,)


class CopyTermsOfService(admin.CopyObject):
    def update(self, request, instance, original):
        instance.version = ' '.join(['+ ', original.version])
        instance.status = TermsOfService.DRAFT

    def update_m2m(self, request, instance, original):
        for option in original.options.all():
            instance.options.add(option)


class TermsOfServiceTranslationInlineForm(forms.ModelForm):
    pass


class TermsOfServiceTranslationInline(admin.StackedInline):
    form = TermsOfServiceTranslationInlineForm
    model = TermsOfServiceTranslation
    extra = 0
    max_num = LANG


class TermsOfServiceAdminForm(forms.ModelForm):
    pass


@admin.register(TermsOfService)
class TermsOfServiceAdmin(admin.ModelAdmin):
    form = TermsOfServiceAdminForm
    inlines = (TermsOfServiceTranslationInline,)
    filter_horizontal = ('options',)
    list_display = ('version', 'status', 'date_begin', 'date_end')
    list_editable = ('status', 'date_begin', 'date_end')
    actions = [CopyTermsOfService()]


class UserAgreementOptionInlineForm(forms.ModelForm):
    pass


class UserAgreementOptionInline(admin.TabularInline):
    form = UserAgreementOptionInlineForm
    model = UserAgreementOption

    def get_max_num(self, request, obj=None, **kwargs):
        return obj.tos.options.count() if obj is not None else 0


class UserAgreementAdminForm(forms.ModelForm):
    pass


@admin.register(UserAgreement)
class UserAgreementAdmin(admin.ModelAdmin):
    form = UserAgreementAdminForm
    search_fields = ('user__pk', 'user__username', 'user__first_name', 'user__last_name', 'user__email')
    list_display = ('user', 'created_at', '_version', '_options')
    related_search_fields = {
        'tos': ('pk', 'version'),
        'user': ('pk', 'username', 'first_name', 'last_name', 'email'),
    }
    inlines = (UserAgreementOptionInline,)

    def _version(self, obj):
        return '%s' % obj.tos.version
    _version.allow_tags = True
    _version.short_description = _('version')

    def _options(self, obj):
        options = ['%s: %s' % (option.option.translate().key, option.value) for option in obj.options.all()]
        return '<br>'.join(options)
    _options.allow_tags = True
    _options.short_description = _('options')
