# -*- coding: utf-8 -*-
import logging

from plone import api
from plone.dexterity.interfaces import IDexterityFTI

logger = logging.getLogger('collective.dms.scanbehavior: upgrade. ')


def v2(context):
    setup = api.portal.get_tool('portal_setup')
    setup.runImportStepFromProfile('profile-collective.dms.scanbehavior:default', 'catalog')
    catalog = api.portal.get_tool('portal_catalog')
    ftis = api.portal.get_tool('portal_types')
    types = []
    for fti in ftis.listTypeInfo():
        if (IDexterityFTI.providedBy(fti) and
                "collective.dms.scanbehavior.behaviors.behaviors.IScanFields" in fti.behaviors):
            types.append(fti.getId())

    nb = 0
    for brain in catalog.searchResults(portal_type=types):
        nb += 1
        obj = brain.getObject()
        obj.reindexObject(idxs=['signed'])
    logger.info("%d objects were migrated" % nb)

