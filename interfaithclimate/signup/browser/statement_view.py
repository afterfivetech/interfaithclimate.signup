from five import grok
from plone.directives import dexterity, form
from interfaithclimate.signup.content.statement import IStatement
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IStatement)
    grok.require('zope2.View')
    grok.template('statement_view')
    grok.name('view')

    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def statement_results(self):
        context = self.context
        catalog = self.catalog
	path = '/'.join(context.getPhysicalPath())
	brains = catalog.searchResults(path={'query':path, 'depth':2}, portal_type='interfaithclimate.signup.signature' , review_state='published')
	return brains





