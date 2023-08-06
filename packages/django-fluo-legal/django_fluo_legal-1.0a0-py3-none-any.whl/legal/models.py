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
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from fluo.db import models
from fluo.urls import reverse


class NoActiveTermsOfService(ValidationError):
        pass


class Option(models.TimestampModel, models.I18NModel, models.OrderedModel):
    key = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name=_('key'),
    )
    required = models.BooleanField(
        default=False,
        verbose_name=_('required'),
    )
    default = models.BooleanField(
        default=False,
        verbose_name=_('default value'),
    )
    label = models.TextField(
        verbose_name=_('label'),
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('description'),
    )
    error_message = models.TextField(
        blank=True,
        default='',
        verbose_name=_('error message'),
    )

    class Meta:
        ordering = ('ordering',)
        unique_together = ('ordering', 'key')
        verbose_name = _('option')
        verbose_name_plural = _('options')

    def __str__(self):
        return self.key


class OptionTranslation(models.TranslationModel):
    parent = models.ForeignKey(
        Option,
        db_index=True,
        on_delete=models.CASCADE,
        related_name='translations',
        verbose_name=_('option'),
    )
    label = models.TextField(
        verbose_name=_('label'),
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('description'),
    )
    error_message = models.TextField(
        blank=True,
        default='',
        verbose_name=_('error message'),
    )

    class Meta:
        unique_together = ('parent', 'language')
        verbose_name = _('translation')
        verbose_name_plural = _('translations')

    def __str__(self):
        return "%s %s translation" % (self.language, self.parent)


class TermsOfServiceManager(models.Manager):
    def _filter(self, status, order_by=None):
        now = timezone.now()
        q1 = Q(Q(date_begin__isnull=True) | Q(date_begin__lte=now))
        q2 = Q(Q(date_end__isnull=True) | Q(date_end__gte=now))
        qs = self.filter(Q(status=status) & q1 & q2)
        if order_by is not None:
            qs = qs.order_by(order_by)
        return qs

    def draft(self, order_by=None):
        return self._filter(status=TermsOfService.DRAFT, order_by=order_by)

    def published(self, order_by=None):
        return self._filter(status=TermsOfService.PUBLISHED, order_by=order_by)

    def latest(self, **kwargs):
        try:
            return self.filter(**kwargs).order_by('-date_begin')[0]
        except (self.model.DoesNotExist, IndexError):
            raise self.model.DoesNotExist

    @property
    def current(self):
        try:
            return self.published()[0]
        except (self.model.DoesNotExist, IndexError):
            raise NoActiveTermsOfService('Please create an active Terms-of-Service')


class TermsOfService(models.TimestampModel, models.I18NModel):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    REVIEW = 'review'
    STATUS_CHOICES = (
        (DRAFT, _('Draft')),
        (REVIEW, _('Review')),
        (PUBLISHED, _('Published')),
    )

    objects = TermsOfServiceManager()

    status = models.StatusField(
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text=_('If should be displayed or not.'),
    )
    version = models.CharField(
        max_length=15,
        unique=True,
        db_index=True,
        verbose_name=_('version'),
    )
    date_begin = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('date begin'),
        help_text=_('When TOS begins to be effective.'),
    )
    date_end = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Date end'),
        help_text=_('When TOS ends to be effective.'),
    )
    label = models.TextField(
        blank=True,
        default='',
        verbose_name=_('label'),
    )
    title = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name=_('Title'),
    )
    text = models.TextField(
        blank=True,
        default='',
        verbose_name=_('Default text'),
    )
    human_title = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name=_('human title'),
        help_text=_('human readable tos title'),
    )
    human_text = models.TextField(
        blank=True,
        default='',
        verbose_name=_('human text'),
        help_text=_('human readable tos text'),
    )
    changelog = models.TextField(
        blank=True,
        default='',
        verbose_name=_('changelog'),
        help_text=_('difference(s) from previous version'),
    )
    options = models.ManyToManyField(
        Option,
        blank=True,
        verbose_name=_('options'),
    )

    class Meta:
        ordering = ("-date_begin", "-version")
        verbose_name = _('TermsOfService')
        verbose_name_plural = _('TermsOfService')

    def __str__(self):
        return 'Terms of Service %(version)s %(from)s [%(status)s]' % {
            'from': self.date_begin,
            'version': self.version,
            'status': self.get_status_display(),
        }

    @property
    def active(self):
        current = TermsOfService.objects.current
        return self.id == current.id

    def get_absolute_url(self):
        return reverse('tos-detail', kewarg={'slug': self.translate().slug})
    absolute_url = property(get_absolute_url)

    def get_preview_url(self):
        return reverse('tos-preview', kwargs={'slug': self.translate().slug, 'token': self.uuid})
    preview_url = property(get_preview_url)

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.date_begin and self.status == TermsOfService.PUBLISHED:
            self.date_begin = now
        super().save(*args, **kwargs)

    def publish(self, *args, **kwargs):
        self.status = TermsOfService.PUBLISHED
        self.save(*args, **kwargs)

    def unpublish(self, *args, **kwargs):
        self.status = TermsOfService.DRAFT
        self.save(*args, **kwargs)

    @property
    def prev(self):
        try:
            tos = TermsOfService.objects.published()[1]
        except IndexError:
            raise TermsOfService.DoesNotExist()
        return tos


class TermsOfServiceTranslation(models.TranslationModel):
    parent = models.ForeignKey(
        TermsOfService,
        db_index=True,
        on_delete=models.CASCADE,
        related_name='translations',
        verbose_name=_('TermsOfService'),
    )
    label = models.TextField(
        blank=True,
        default='',
        verbose_name=_('label'),
    )
    title = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name=_('legal title'),
        help_text=_('legal tos title'),
    )
    text = models.TextField(
        blank=True,
        default='',
        verbose_name=_('legal text'),
        help_text=_('legal tos text'),
    )
    human_title = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name=_('human title'),
        help_text=_('human readable tos title'),
    )
    human_text = models.TextField(
        blank=True,
        default='',
        verbose_name=_('human text'),
        help_text=_('human readable tos text'),
    )
    changelog = models.TextField(
        blank=True,
        default='',
        verbose_name=_('changelog'),
        help_text=_('difference(s) from previous version'),
    )

    class Meta:
        unique_together = (('language', 'parent'), ('human_title', 'human_text'))
        verbose_name = _('TermsOfService Translation')
        verbose_name_plural = _('TermsOfService Translations')

    def __str__(self):
        return self.title


class UserAgreement(models.TimestampModel):
    tos = models.ForeignKey(
        TermsOfService,
        db_index=True,
        on_delete=models.CASCADE,
        related_name='terms',
        verbose_name=_('tos'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_index=True,
        on_delete=models.CASCADE,
        related_name='user_agreements',
        verbose_name=_('user'),
    )

    class Meta:
        unique_together = ('user', 'tos')
        ordering = ["-created_at"]

    def __str__(self):
        return '%(user)s agreed to TermsOfService %(tos)s at %(when)s' % {
            'user': self.user.username,
            'tos': self.tos,
            'when': self.created_at,
        }


class UserAgreementOption(models.Model):
    parent = models.ForeignKey(
        UserAgreement,
        db_index=True,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name=_('user agreement'),
    )
    option = models.ForeignKey(
        Option,
        db_index=True,
        on_delete=models.CASCADE,
        related_name='user_agreements',
        verbose_name=_('user agreement'),
    )
    value = models.BooleanField(
        default=False,
        verbose_name=_('value'),
    )

    def __str__(self):
        return '%(version)s %(option)s: %(value)s' % {
            'version': self.parent.tos.version,
            'option': self.option,
            'value': self.value,
        }


def has_user_agreed_latest_tos(user):
    return UserAgreement.objects.filter(
        tos=TermsOfService.objects.current,
        user=user,
    ).exists()
