# -*- coding: utf-8 -*-
"""Test Layer for plone.mls.core."""

from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer


class PloneMLSCore(PloneSandboxLayer):
    """Custom Test Layer for plone.mls.core."""
    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        """Set up Zope for testing."""
        # Load ZCML
        import plone.mls.core
        self.loadZCML(package=plone.mls.core)

    def setUpPloneSite(self, portal):
        """Set up a Plone site for testing."""
        applyProfile(portal, 'plone.mls.core:default')


PLONE_MLS_CORE_FIXTURE = PloneMLSCore()
PLONE_MLS_CORE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_MLS_CORE_FIXTURE, ),
    name='PloneMLSCore:Integration',
)
