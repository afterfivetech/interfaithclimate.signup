from five import grok
from plone.directives import dexterity, form
from interfaithclimate.signup.content.signature import ISignature

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(ISignature)
    grok.require('zope2.View')
    grok.template('signature_view')
    grok.name('view')

