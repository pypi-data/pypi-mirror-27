# -*- coding: utf-8 -*-

from collective.ambidexterity import audit
from collective.ambidexterity import default_script
from collective.ambidexterity import models
from collective.ambidexterity import validator_script
from collective.ambidexterity import vocabulary_script
from collective.ambidexterity import view as ad_view
from collective.ambidexterity.utilities import getAmbidexterityFile
from collective.ambidexterity.utilities import getResourcesInventory
from plone.protect import CheckAuthenticator
from plone.protect import PostOnly
from plone.protect.utils import addTokenToUrl
from Products.Five import BrowserView

import json


class EditorView(BrowserView):
    """Editor view.
    """

    def tokenizedURL(self, url):
        return addTokenToUrl(url)

    def resource_url(self):
        url = self.context.absolute_url() + "/@@ambidexterityajax/resource_inventory"
        return addTokenToUrl(url)

    def audit_is_clean(self):
        audit_rez = audit.auditResourceModelMatch()
        return audit.auditIsClean(audit_rez)

    def audit_report(self):
        return audit.readableAuditReport()


class ResyncView(BrowserView):
    """Resynchronization view.
    """

    def __call__(self):
        PostOnly(self.request)
        CheckAuthenticator(self.request)
        audit.resynchronize_all()
        self.request.RESPONSE.redirect(self.context.absolute_url() + '/@@ambidexterityeditor')


class EditorAjax(BrowserView):
    """ AJAX support
    """

    def __call__(self):
        return None

    def resource_inventory(self):
        """ Return inventory in JSON
        """

        CheckAuthenticator(self.request)

        self.request.RESPONSE.setHeader(
            'Content-Type',
            'application/json'
        )
        self.request.RESPONSE.setHeader(
            'Cache-Control',
            'no-cache'
        )
        return json.dumps(getResourcesInventory())

    def button_action(self):
        """ Respond to button clicks.
        """

        PostOnly(self.request)
        CheckAuthenticator(self.request)

        form = self.request.form
        button_id = form['button_id']
        content_type = form['content_type']
        field_name = form['field_name']

        result = {}

        if button_id == 'add_default':
            default_script.addDefaultScript(content_type, field_name)
            models.setDefaultFactory(content_type, field_name)
        elif button_id == 'remove_default':
            default_script.rmDefaultScript(content_type, field_name)
            models.removeDefaultFactory(content_type, field_name)
        elif button_id == 'edit_default':
            result = dict(
                action='edit',
                source=getAmbidexterityFile(content_type, field_name, 'default.py'),
            )
        elif button_id == 'add_validator':
            validator_script.addValidatorScript(content_type, field_name)
            models.setValidator(content_type, field_name)
        elif button_id == 'remove_validator':
            validator_script.rmValidatorScript(content_type, field_name)
            models.removeValidator(content_type, field_name)
        elif button_id == 'edit_validator':
            result = dict(
                action='edit',
                source=getAmbidexterityFile(content_type, field_name, 'validate.py'),
            )
        elif button_id == 'add_vocabulary':
            vocabulary_script.addVocabularyScript(content_type, field_name)
            models.setVocabulary(content_type, field_name)
        elif button_id == 'remove_vocabulary':
            vocabulary_script.rmVocabularyScript(content_type, field_name)
            models.removeVocabulary(content_type, field_name)
        elif button_id == 'edit_vocabulary':
            result = dict(
                action='edit',
                source=getAmbidexterityFile(content_type, field_name, 'vocabulary.py'),
            )
        elif button_id == 'add_view':
            ad_view.addViewTemplate(content_type)
            models.setAmbidexterityView(content_type)
        elif button_id == 'edit_view':
            result = dict(
                action='edit',
                source=getAmbidexterityFile(content_type, None, 'view.pt'),
            )
        elif button_id == 'remove_view':
            ad_view.rmViewTemplate(content_type)
            models.removeAmbidexterityView(content_type)

        self.request.RESPONSE.setHeader(
            'Content-Type',
            'application/json'
        )
        self.request.RESPONSE.setHeader(
            'Cache-Control',
            'no-cache'
        )
        return json.dumps(result)

    def save_action(self):
        """ Save a script.
        """

        PostOnly(self.context.REQUEST)
        CheckAuthenticator(self.request)

        form = self.request.form
        content_type = form['content_type']
        field_name = form['field_name']
        script = form['script']
        body = form['data']

        result = 'failure'
        if script == 'edit_default':
            default_script.updateDefaultScript(content_type, field_name, body)
            result = 'success'
        elif script == 'edit_validator':
            validator_script.updateValidatorScript(content_type, field_name, body)
            result = 'success'
        elif script == 'edit_vocabulary':
            vocabulary_script.updateVocabularyScript(content_type, field_name, body)
            result = 'success'
        elif script == 'edit_view':
            ad_view.updateViewTemplate(content_type, body)
            result = 'success'

        result = dict(result=result)
        self.request.RESPONSE.setHeader(
            'Content-Type',
            'application/json'
        )
        self.request.RESPONSE.setHeader(
            'Cache-Control',
            'no-cache'
        )
        return json.dumps(result)
