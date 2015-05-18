from zope.formlib import form
from zope import schema
from zope.interface import implements
from zope.component import getMultiAdapter
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class IBurgerMenuPortlet(IPortletDataProvider):
    
    path = schema.TextLine(
        title = u"URL of Pilgrimage Home"
    )


class Assignment(base.Assignment):
    implements(IBurgerMenuPortlet)
    
    def __init__(self, path=None):
        self.path = path
        
    title = u"Burger Menu Portlet"
    

class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/burgermenuportlet.pt')
    
    def __init__(self, context, request, view, manager, data):
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        self.data = data
        
    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')
    
    def pilgrimage_steps(self):
        results  = []
        path = self.data.path
        brains = self.catalog.unrestrictedSearchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.pilgrimagesteps')
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            parent = obj.aq_parent
            data = {'position':parent.getObjectPosition(brain.id) + 1}
            data['title'] = brain.Title
            data['url'] = brain.getPath()
            data['obj'] = obj
            data['image'] = obj.image
            
            results.append(data)
        if results:
            results.sort(key=lambda result:result['position'])
        return results
    

class AddForm(base.AddForm):
    form_fields = form.Fields(IBurgerMenuPortlet)
    label = u"Add Burger Menu Portlet"
    description = ''
    
    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment


    
    