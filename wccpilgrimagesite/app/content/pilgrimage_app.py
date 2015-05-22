from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
#from plone.multilingualbehavior.directives import languageindependent
from collective import dexteritytextindexer
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from zope.app.container.interfaces import IObjectAddedEvent
from zope.component import getUtility, getMultiAdapter
from zope.container.interfaces import INameChooser
from plone.portlets.interfaces import IPortletManager, IPortletAssignmentMapping, IPortletRetriever
from wccpilgrimagesite.app.portlet import burgermenuportlet

from wccpilgrimagesite.app import MessageFactory as _
from Products.CMFCore.utils import getToolByName
from plone.i18n.normalizer import idnormalizer


# Interface class; used to define content-type schema.

class IPilgrimageApp(form.Schema, IImageScaleTraversable):
    """
    Pilgrimage App
    """
    url_label = schema.TextLine(
        title=u'Url Label',
        required=True,
    )

    form.widget(body=WysiwygFieldWidget)
    body = schema.Text(title=u"Description",
    required=False,
    )

    pass

alsoProvides(IPilgrimageApp, IFormFieldProvider)

@grok.subscribe(IPilgrimageApp, IObjectAddedEvent)
def _createObj(context, event):
    parent = context.aq_parent
    column = getUtility(IPortletManager, name=u'plone.leftcolumn', context=context)
    manager = getMultiAdapter((context, column,), IPortletAssignmentMapping)
    assignment = burgermenuportlet.Assignment()
    chooser = INameChooser(manager)
    assignment.path = '/'.join(context.getPhysicalPath())
    manager[chooser.chooseName(None, assignment)] = assignment

    id = context.getId()
    object_Ids = []
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog.unrestrictedSearchResults(object_provides = IPilgrimageApp.__identifier__)
    for brain in brains:
        object_Ids.append(brain.id)
    
    last_name = str(idnormalizer.normalize(context.title))
    temp_new_id = last_name
    new_id = temp_new_id.replace("-","")
    test = ''
    if new_id in object_Ids:
        test = filter(lambda name: new_id in name, object_Ids)
        if '-' not in (max(test)):
            new_id = new_id + '-1'
        if '-' in (max(test)):
            new_id = new_id +'-' +str(int(max(test).split('-')[-1])+1) 

    parent.manage_renameObject(id, new_id )
    new_title = last_name
    context.setTitle(context.title)


    context.reindexObject()
    return


