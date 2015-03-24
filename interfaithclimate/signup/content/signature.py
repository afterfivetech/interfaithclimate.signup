from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides

from zope.interface import invariant, Invalid

import z3c.form
from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.multilingualbehavior.directives import languageindependent
from collective import dexteritytextindexer

from interfaithclimate.signup import MessageFactory as _
from quintagroup.z3cform.captcha import Captcha, CaptchaWidgetFactory
from interfaithclimate.signup.interfaces import ICaptchaSchema

import re
from zope.schema import ValidationError
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid
from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from plone.i18n.normalizer import idnormalizer


class InvalidEmailAddress(ValidationError):
    "Invalid email address"


def validateaddress(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True

# Interface class; used to define content-type schema.

class ISignature(form.Schema, IImageScaleTraversable):
    """
    Signature
    """

    first_name = schema.TextLine(
           title=_(u"First Name"),
           required=True,
        )

    last_name = schema.TextLine(
           title=_(u"Last Name"),
           required=True,
        )

    organization = schema.TextLine(
           title=_(u"Organization"),
           required=False,
        )

    designation = schema.TextLine(
           title=_(u"Designation"),
           required=False,
        )

    # city = schema.TextLine(
    #        title=_(u"City"),
    #        required=False,
    #     )

    country = schema.TextLine(
           title=_(u"Country"),
           required=False,
        )

    email1 = schema.TextLine(
           title=_(u"Email Address"),
           constraint=validateaddress,
        )

    email2 = schema.TextLine(
           title=_(u"Enter the same email address"),
           constraint=validateaddress
        )

    
    
    captcha = Captcha(
        title=_(u'Type the code'),
        description=_(u'Type the code from the picture shown below.'))
    
    @invariant
    def emailAddressValidation(self):
        #pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            
        if self.email1 != self.email2:
            raise Invalid(_("Both email addresses do not match"))
        
        #if not bool(re.match(pattern, self.email1)):
        #    raise Invalid(_(u"Email 1 is not a valid email address."))
        #elif not bool(re.match(pattern, self.email2  )):
        #    raise Invalid(_(u"Email 2 is not a valid email address."))
    
    pass

alsoProvides(ISignature, IFormFieldProvider)

@form.default_value(field = IExcludeFromNavigation['exclude_from_nav'])
def excludeFromNavDefaultValue(data):
    return data.request.URL.endswith('++add++interfaithclimate.signup.signature')

class SignatureForm(z3c.form.form.Form):
    fields = z3c.form.field.Fields(ISignature)
    
    fields["captcha"].widgetFactory = CaptchaWidgetFactory
    

@grok.subscribe(ISignature, IObjectAddedEvent)
def _createObject(context, event):
    parent = context.aq_parent
    id = context.getId()
    object_Ids = []
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog.unrestrictedSearchResults(object_provides = ISignature.__identifier__)
    for brain in brains:
        object_Ids.append(brain.id)
    
    last_name = idnormalizer.normalize(context.last_name)
    first_name = idnormalizer.normalize(context.first_name)
    new_id = last_name+'_'+first_name
    test = ''
    if new_id in object_Ids:
        test = filter(lambda name: new_id in name, object_Ids)
        
        if '-' not in (max(test)):
            new_id = new_id + '-1'
        if '-' in (max(test)):
            new_id = new_id +'-' +str(int(max(test).split('-')[1])+1)  
    parent.manage_renameObject(id, new_id )
    new_title = last_name+' '+first_name
    context.setTitle(new_title)

    #exclude from navigation code
    behavior = IExcludeFromNavigation(context)
    behavior.exclude_from_nav = True

    context.reindexObject()
    return

@grok.subscribe(ISignature, IObjectModifiedEvent)
def modifyobject(context, event):
    parent = context.aq_parent
    id = context.getId()
    object_Ids = []
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog.unrestrictedSearchResults(object_provides = ISignature.__identifier__)
    for brain in brains:
        object_Ids.append(brain.id)
    
    last_name = idnormalizer.normalize(context.last_name)
    first_name = idnormalizer.normalize(context.first_name)
    new_id = last_name+'_'+first_name
    test = ''
    if new_id in object_Ids:
        test = filter(lambda name: new_id in name, object_Ids)
        
        if '-' not in (max(test)):
            new_id = new_id + '-1'
        if '-' in (max(test)):
            new_id = new_id +'-' +str(int(max(test).split('-')[1])+1)  
    parent.manage_renameObject(id, new_id )
    new_title = last_name+' '+first_name
    context.setTitle(new_title)
    context.reindexObject()
    return
