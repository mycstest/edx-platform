"""
Specialized models for oauth_dispatch djangoapp
"""

from datetime import datetime
from django.db import models
from pytz import utc

from oauth2_provider.settings import oauth2_settings
from django.utils.translation import ugettext_lazy as _

class RestrictedApplication(models.Model):
    """
    This model lists which django-oauth-toolkit Applications are considered 'restricted'
    and thus have a limited ability to use various APIs.

    A restricted Application will only get expired token/JWT payloads
    so that they cannot be used to call into APIs.
    """

    application = models.ForeignKey(oauth2_settings.APPLICATION_MODEL, null=False)

    def __unicode__(self):
        """
        Return a unicode representation of this object
        """
        return u"<RestrictedApplication '{name}'>".format(
            name=self.application.name
        )

    @classmethod
    def set_access_token_as_expired(cls, access_token):
        """
        For access_tokens for RestrictedApplications, put the expire timestamp into the beginning of the epoch
        which is Jan. 1, 1970
        """
        access_token.expires = datetime(1970, 1, 1, tzinfo=utc)

    @classmethod
    def verify_access_token_as_expired(cls, access_token):
        """
        For access_tokens for RestrictedApplications, make sure that the expiry date
        is set at the beginning of the epoch which is Jan. 1, 1970
        """
        return access_token.expires == datetime(1970, 1, 1, tzinfo=utc)

"""
Django models for the dot-restrict-scopes package.
"""

from django.db import models

from oauth2_provider.models import AbstractApplication
from oauth2_provider.scopes import get_scopes_backend

_DEFAULT_SEPARATOR = ' '

class RestrictedApplication_2(AbstractApplication):
    """
    Application model for use with Django OAuth Toolkit that allows the scopes
    available to an application to be restricted on a per-application basis.
    """
    allowed_scope = models.TextField(blank = True)
    """
    @property
    def allowed_scopes(self):
        Returns the set of allowed scope names for this application.
        all_scopes = set(get_scopes_backend().get_all_scopes().keys())
        app_scopes = set(self.allowed_scope.split())
        return app_scopes.intersection(all_scopes)
    """
    def _get_list_from_delimited_string(self, delimited_string, separator=_DEFAULT_SEPARATOR):
        """
        Helper to return a list from a delimited string
        """

        return delimited_string.split(separator) if delimited_string else []
    
    def allowed_scopes(self):
        """
        Translate space delimited string to a list
        """
        all_scopes = set(get_scopes_backend().get_all_scopes().keys())
        app_scopes = set(self._get_list_from_delimited_string(self.allowed_scope))
        return app_scopes.intersection(all_scopes)


from organizations.models import Organization

class RestrictedApplication_33(models.Model):

    CONTENT_PROVIDER = 'content_provider'
    USER_PROVIDER = 'user_provider'
    ORGANIZATION_PROVIDER_TYPES = (
        (CONTENT_PROVIDER, _('Content Provider')),
        (USER_PROVIDER, _('User Provider')),
    )
    application = models.ForeignKey(oauth2_settings.APPLICATION_MODEL, null=False)

    _org_associations = models.ManyToManyField(Organization)

    organization_type = models.CharField(max_length=32, choices=ORGANIZATION_PROVIDER_TYPES, default=CONTENT_PROVIDER)

    @property
    def org_associations(self):
        """
        Translate space delimited string to a list
        """
        org_associations_list = []
        for each in self._org_associations.all():
            org_associations_list.append(each.name)
        return org_associations_list
