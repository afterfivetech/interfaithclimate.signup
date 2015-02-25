from five import grok
from plone.directives import dexterity, form
from interfaithclimate.signup.content.statement import IStatement

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IStatement)
    grok.require('zope2.View')
    grok.template('statement_view')
    grok.name('view')

