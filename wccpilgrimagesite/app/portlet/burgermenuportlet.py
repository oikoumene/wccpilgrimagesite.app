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
        brains = self.catalog.unrestrictedSearchResults(path={'query':path, 'depth':1}, portal_type=('wccpilgrimagesite.app.pilgrimagesteps', 'wccpilgrimagesite.app.burgerlinks'))
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            parent = obj.aq_parent
            data = {'position':parent.getObjectPosition(brain.id) + 1}
            
            if brain.portal_type == 'wccpilgrimagesite.app.pilgrimagesteps':
                data['title'] = str(data['position'])+'. '+brain.Title
                data['url'] = brain.getPath()
            else:
                data['title'] = brain.Title
                data['url'] = obj.burger_link_url
            #data['obj'] = obj
            #data['image'] = obj.image
            
            results.append(data)
        if results:
            results.sort(key=lambda result:result['position'])
        return results
    
    def home_link(self, ):
        portal_state = getMultiAdapter((self.context, self.request), name="plone_portal_state")
        path = portal_state.navigation_root_path()
        brains = self.catalog.unrestrictedSearchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.pilgrimageapp')
        
        for brain in brains:
            return brain.getPath()
        return '#'
    
    

class AddForm(base.AddForm):
    form_fields = form.Fields(IBurgerMenuPortlet)
    label = u"Add Burger Menu Portlet"
    description = ''
    
    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment
    
class EditForm(base.EditForm):
    form_fields = form.Fields(IBurgerMenuPortlet)
    label = u"Edit Burger Menu Portlet"
    description = ''


    
    