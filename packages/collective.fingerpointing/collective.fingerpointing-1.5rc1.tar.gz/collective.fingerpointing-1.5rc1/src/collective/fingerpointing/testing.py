# -*- coding: utf-8 -*-
"""Setup testing infrastructure.

For Plone 5 we need to install plone.app.contenttypes.
"""
from plone import api
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import os
import pkg_resources
import shutil
import tempfile


try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    from plone.app.testing import PLONE_FIXTURE
else:
    from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE as PLONE_FIXTURE  # noqa: E501


IS_PLONE_5 = api.env.plone_version().startswith('5')


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    # XXX: this can probably be done in a different way
    def _setup_audit_log(self):
        """Fake configuration for collective.fingerpointing as tests
        expect an audit.log file to be set.
        """
        from collective.fingerpointing.config import fingerpointing_config
        from collective.fingerpointing.logger import log_info
        self.temp_dir = tempfile.mkdtemp()
        fingerpointing_config['audit-log'] = os.path.join(
            self.temp_dir,
            'audit.log',
        )
        log_info.configure(fingerpointing_config)

    def _cleanup_audit_log(self):
        from collective.fingerpointing.config import fingerpointing_config
        fingerpointing_config['audit-log'] = None
        shutil.rmtree(self.temp_dir)

    def setUpZope(self, app, configurationContext):
        self._setup_audit_log()
        import collective.fingerpointing
        self.loadZCML(package=collective.fingerpointing)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.fingerpointing:default')
        portal.portal_workflow.setDefaultChain('simple_publication_workflow')

    def tearDown(self):
        super(Fixture, self).tearDown()
        self._cleanup_audit_log()


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name='collective.fingerpointing:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name='collective.fingerpointing:Functional')

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='collective.fingerpointing:Robot',
)
