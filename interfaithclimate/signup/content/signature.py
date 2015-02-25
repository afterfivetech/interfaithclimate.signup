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

# Interface class; used to define content-type schema.

class ISignature(form.Schema, IImageScaleTraversable):
    """
    Signature
    """

    first_name = schema.TextLine(
           title=_(u"First Name"),
           required=False,
        )

    last_name = schema.TextLine(
           title=_(u"Last Name"),
           required=False,
        )

    organization = schema.TextLine(
           title=_(u"Organization"),
           required=False,
        )

    designation = schema.TextLine(
           title=_(u"Designation"),
           required=False,
        )

    city = schema.TextLine(
           title=_(u"City"),
           required=False,
        )

    country = schema.TextLine(
           title=_(u"Country"),
           required=False,
        )

    email1 = schema.TextLine(
           title=_(u"Email Address 1"),
        )

    email2 = schema.TextLine(
           title=_(u"Email Address 2"),
        )

    
    
    captcha = Captcha(
        title=_(u'Type the code'),
        description=_(u'Type the code from the picture shown below.'))
    
    @invariant
    def emailAddressValidation(self):
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            
        if self.email1 != self.email2:
            raise Invalid(_("Email 1 and Email 2 addresses are not the same."))
        
        if not bool(re.match(pattern, self.email1)):
            raise Invalid(_(u"Email 1 is not a valid email address."))
        
        elif not bool(re.match(pattern, self.email2  )):
            raise Invalid(_(u"Email 2 is not a valid email address."))
    
    pass

alsoProvides(ISignature, IFormFieldProvider)

class SignatureForm(z3c.form.form.Form):
    fields = z3c.form.field.Fields(ISignature)
    
    fields["captcha"].widgetFactory = CaptchaWidgetFactory
