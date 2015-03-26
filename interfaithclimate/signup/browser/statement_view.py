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

        brains = catalog.searchResults(path={'query':path, 'depth':2}, portal_type='interfaithclimate.signup.signature', review_state='published')
        results = []
        results1 = []
        for brain1 in brains:
            obj = brain1._unrestrictedGetObject()
            value = ''
            value1 = ''
            if obj.first_name and obj.last_name:
                value += '%s %s' % (obj.first_name,obj.last_name)
            if obj.designation:
                value1 += ', '+obj.designation
            if obj.organization:
                value1 += ', '+obj.organization
     #    if obj.city:
        # value += ', '+str(obj.city)
            if obj.country:
                value1 += ', '+obj.country
            if value:
                results.append({'value':value, 'value1': value1})
           
        return results






