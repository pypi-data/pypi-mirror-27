# -*- coding: utf-8 -*-
"""Additional setup steps."""

from logging import getLogger
from plone.browserlayer import utils as layerutils
from plone.mls.core.browser.interfaces import IMLSSpecific
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


logger = getLogger('plone.mls.core')


def resetLayers(context):
    """Remove custom browser layer on uninstall."""

    if context.readDataFile('plone.mls.core_uninstall.txt') is None:
        return

    if IMLSSpecific in layerutils.registered_layers():
        layerutils.unregister_layer(name='plone.mls.core')
        logger.info('Browser layer "plone.mls.core" uninstalled.')


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'plone.mls.core:default',
            'plone.mls.core:install-base',
            'plone.mls.core:uninstall',
            'plone.mls.core:uninstall-base',
        ]
