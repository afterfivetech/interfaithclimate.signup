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
	for brain1 in brains:
            obj = brain1._unrestrictedGetObject()
	    value = ''
	    if obj.first_name and obj.last_name:
		value += '%s %s' % (obj.first_name,obj.last_name)
	    if obj.designation:
		value += ', '+str(obj.designation)
	    if obj.organization:
		value += ', '+str(obj.organization)
	 #    if obj.city:
		# value += ', '+str(obj.city)
	    if obj.country:
		value += ', '+str(obj.country)
	    if value:
		results.append(value)
            # results.append({'first_name': obj.first_name,
            #                    'last_name': obj.last_name,
            #                    'organization': obj.organization,
            #                    'designation': obj.designation,
            #                    # 'city':obj.city,
            #                    'country': obj.country,
            #                    'email1':obj.email1})
        return results







