# codign: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class CompiledDescriptionMixIn(models.Model):

    description = models.TextField(
        verbose_name=_('Description'),
        null=True
    )

    _cached_description = models.TextField(
        verbose_name=_('Cached Description'),
        null=True
    )

    def compile_description(self):
        raise NotImplementedError

    class Meta:
        abstract = True


class CreatedByMixIn(models.Model):

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:

        abstract = True


class DateCreatedMixIn(models.Model):

    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date Created')
    )

    class Meta:

        abstract = True


class DateUpdatedMixIn(models.Model):

    date_updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Date Updated')
    )

    class Meta:

        abstract = True


class DateRangeMixIn(models.Model):

    start_date = models.DateTimeField(
        verbose_name=_('Start Date'),
        null=True
    )

    end_date = models.DateTimeField(
        verbose_name=_('End Date'),
        null=True
    )

    class Meta:
        abstract = True


class DomainModelMixIn(DateCreatedMixIn,
                       DateUpdatedMixIn):

    code = models.CharField(
        max_length=32,
        verbose_name=_('Code'),
        unique=True
    )

    description = models.CharField(
        max_length=128,
        verbose_name=_('Description'),
        null=True
    )

    def __unicode__(self):

        return u'{0} ({1})'.format(self.code, self.description)

    class Meta:

        abstract = True


class BaseURL(CreatedByMixIn,
              DateCreatedMixIn,
              DateUpdatedMixIn):

    name = models.CharField(
        max_length=64,
        verbose_name=_('Name')
    )

    uri = models.URLField(
        max_length=128,
        verbose_name=_('URL'),
        null=True
    )

    def __unicode__(self):

        return self.name

    class Meta:
        abstract = True


class BasePhone(CreatedByMixIn,
                DateCreatedMixIn,
                DateUpdatedMixIn):

    contact = models.CharField(
        verbose_name=_('Contact'),
        max_length=128,
        null=True
    )

    phone = PhoneNumberField(
        verbose_name=_('Phone Number'),
        null=True
    )

    def __unicode__(self):

        return self.phone

    class Meta:
        abstract = True
