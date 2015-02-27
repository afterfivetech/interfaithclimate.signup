from five import grok
from plone.directives import dexterity, form
from interfaithclimate.signup.content.signature import ISignature
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(ISignature)
    grok.require('zope2.View')
    grok.template('signature_view')
    grok.name('view')


   


    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def signature_results(self):
        context = self.context
        catalog = self.catalog
	path = '/'.join(context.getPhysicalPath())
	brains = catalog.searchResults(path={'query':path, 'depth':0}, portal_type='interfaithclimate.signup.signature')
	return brains

