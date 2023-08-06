# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.testing import z2

from plone.app.testing import setRoles
from plone.app.testing import applyProfile
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import SITE_OWNER_NAME
# from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import FunctionalTesting
from plone.app.testing import login
from plone.app.testing import logout

from bika.lims.testing import BIKA_LIMS_FUNCTIONAL_TESTING


class SimpleTestLayer(PloneSandboxLayer):
    """Setup Plone with installed AddOn only
    """
    defaultBases = (BIKA_LIMS_FUNCTIONAL_TESTING, PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        super(SimpleTestLayer, self).setUpZope(app, configurationContext)

        # Load ZCML
        import senaite.jsonapi

        self.loadZCML(package=senaite.jsonapi)

        # Install product and call its initialize() function
        z2.installProduct(app, 'senaite.jsonapi')

    def setUpPloneSite(self, portal):
        super(SimpleTestLayer, self).setUpPloneSite(portal)

        # Apply Setup Profile (portal_quickinstaller)
        applyProfile(portal, 'bika.lims:default')
        # applyProfile(portal, 'senaite.jsonapi:default')

        login(portal.aq_parent, SITE_OWNER_NAME)

        # Add some test users
        for role in ('LabManager',
                     'LabClerk',
                     'Analyst',
                     'Verifier',
                     'Sampler',
                     'Preserver',
                     'Publisher',
                     'Member',
                     'Reviewer',
                     'RegulatoryInspector'):
            for user_nr in range(2):
                if user_nr == 0:
                    username = "test_%s" % (role.lower())
                else:
                    username = "test_%s%s" % (role.lower(), user_nr)
                try:
                    member = portal.portal_registration.addMember(
                        username,
                        username,
                        properties={
                            'username': username,
                            'email': username + "@example.com",
                            'fullname': username}
                    )
                    # Add user to all specified groups
                    group_id = role + "s"
                    group = portal.portal_groups.getGroupById(group_id)
                    if group:
                        group.addMember(username)
                    # Add user to all specified roles
                    member._addRole(role)
                    # If user is in LabManagers, add Owner local role on clients folder
                    if role == 'LabManager':
                        portal.clients.manage_setLocalRoles(username,
                                                            ['Owner', ])
                except ValueError:
                    pass  # user exists

    logout()


###
# Use for simple tests (w/o contents)
###
SIMPLE_FIXTURE = SimpleTestLayer()
SIMPLE_TESTING = FunctionalTesting(
    bases=(SIMPLE_FIXTURE, ),
    name="senaite.jsonapi:SimpleTesting"
)


class SimpleTestCase(unittest.TestCase):
    layer = SIMPLE_TESTING

    def setUp(self):
        super(SimpleTestCase, self).setUp()

        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['LabManager', 'Manager'])

    def getBrowser(self, login=True):
        """Instantiate and return a testbrowser for convenience """
        browser = z2.Browser(self.portal)
        browser.addHeader('Accept-Language', 'en-US')
        browser.handleErrors = False
        if login:
            browser.open(self.portal.absolute_url() + "/login_form")
            browser.getControl(name='__ac_name').value = TEST_USER_NAME
            browser.getControl(name='__ac_password').value = TEST_USER_PASSWORD
            browser.getControl(name='submit').click()
            self.assertTrue('You are now logged in' in browser.contents)
        return browser
