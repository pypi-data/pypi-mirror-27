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

import django.utils.timezone
import fluo.db.models.fields
import legal.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', fluo.db.models.fields.OrderField(blank=True, db_index=True, default=0, help_text='Ordered', verbose_name='ordering')),
                ('created_at', fluo.db.models.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('last_modified_at', fluo.db.models.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('key', models.CharField(max_length=255, verbose_name='key', db_index=True)),
                ('required', models.BooleanField(default=False, verbose_name='required')),
                ('default', models.BooleanField(default=False, verbose_name='default value')),
                ('label', models.TextField(verbose_name='label')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('error_message', models.TextField(default='', verbose_name='error message', blank=True)),
            ],
            options={
                'ordering': ('ordering',),
                'verbose_name': 'option',
                'verbose_name_plural': 'options',
            },
        ),
        migrations.CreateModel(
            name='OptionTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(db_index=True, max_length=5, verbose_name='language', choices=settings.LANGUAGES)),
                ('label', models.TextField(verbose_name='label')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('error_message', models.TextField(default='', verbose_name='error message', blank=True)),
                ('parent', models.ForeignKey(on_delete=models.CASCADE, related_name='translations', verbose_name='option', to='legal.Option')),
            ],
            options={
                'verbose_name': 'translation',
                'verbose_name_plural': 'translations',
            },
        ),
        migrations.CreateModel(
            name='TermsOfService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', fluo.db.models.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('last_modified_at', fluo.db.models.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('status', fluo.db.models.fields.StatusField(default=legal.models.TermsOfService.DRAFT, help_text='If should be displayed or not.', max_length=10, verbose_name='status', choices=legal.models.TermsOfService.STATUS_CHOICES)),
                ('version', models.CharField(unique=True, max_length=15, verbose_name='version', db_index=True)),
                ('date_begin', models.DateTimeField(help_text='When TOS begins to be effective.', null=True, verbose_name='date begin', blank=True)),
                ('date_end', models.DateTimeField(help_text='When TOS ends to be effective.', null=True, verbose_name='Date end', blank=True)),
                ('label', models.TextField(default='', verbose_name='label', blank=True)),
                ('title', models.CharField(default='', max_length=255, verbose_name='Title', blank=True)),
                ('text', models.TextField(default='', verbose_name='Default text', blank=True)),
                ('human_title', models.CharField(default='', help_text='human readable tos title', max_length=255, verbose_name='human title', blank=True)),
                ('human_text', models.TextField(default='', help_text='human readable tos text', verbose_name='human text', blank=True)),
                ('changelog', models.TextField(default='', help_text='difference(s) from previous version', verbose_name='changelog', blank=True)),
                ('options', models.ManyToManyField(to='legal.Option', verbose_name='options', blank=True)),
            ],
            options={
                'ordering': ('-date_begin', '-version'),
                'verbose_name': 'TermsOfService',
                'verbose_name_plural': 'TermsOfService',
            },
        ),
        migrations.CreateModel(
            name='TermsOfServiceTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(db_index=True, max_length=5, verbose_name='language', choices=settings.LANGUAGES)),
                ('label', models.TextField(default='', verbose_name='label', blank=True)),
                ('title', models.CharField(default='', help_text='legal tos title', max_length=255, verbose_name='legal title', blank=True)),
                ('text', models.TextField(default='', help_text='legal tos text', verbose_name='legal text', blank=True)),
                ('human_title', models.CharField(default='', help_text='human readable tos title', max_length=255, verbose_name='human title', blank=True)),
                ('human_text', models.TextField(default='', help_text='human readable tos text', verbose_name='human text', blank=True)),
                ('changelog', models.TextField(default='', help_text='difference(s) from previous version', verbose_name='changelog', blank=True)),
                ('parent', models.ForeignKey(on_delete=models.CASCADE, related_name='translations', verbose_name='TermsOfService', to='legal.TermsOfService')),
            ],
            options={
                'verbose_name': 'TermsOfService Translation',
                'verbose_name_plural': 'TermsOfService Translations',
            },
        ),
        migrations.CreateModel(
            name='UserAgreement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', fluo.db.models.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('last_modified_at', fluo.db.models.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('tos', models.ForeignKey(on_delete=models.CASCADE, related_name='terms', verbose_name='tos', to='legal.TermsOfService')),
                ('user', models.ForeignKey(on_delete=models.CASCADE, related_name='user_agreements', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='UserAgreementOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.BooleanField(default=False, verbose_name='value')),
                ('option', models.ForeignKey(on_delete=models.CASCADE, related_name='user_agreements', verbose_name='user agreement', to='legal.Option')),
                ('parent', models.ForeignKey(on_delete=models.CASCADE, related_name='options', verbose_name='user agreement', to='legal.UserAgreement')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='option',
            unique_together=set([('ordering', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='useragreement',
            unique_together=set([('user', 'tos')]),
        ),
        migrations.AlterUniqueTogether(
            name='termsofservicetranslation',
            unique_together=set([('human_title', 'human_text'), ('language', 'parent')]),
        ),
        migrations.AlterUniqueTogether(
            name='optiontranslation',
            unique_together=set([('parent', 'language')]),
        ),
    ]
