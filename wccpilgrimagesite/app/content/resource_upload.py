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

from wccpilgrimagesite.app import MessageFactory as _
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from zope.app.container.interfaces import IObjectAddedEvent
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from zope.interface import invariant, Invalid
import re


from Products.CMFCore.utils import getToolByName
from plone.i18n.normalizer import idnormalizer


# Interface class; used to define content-type schema.

class IResourceUpload(form.Schema, IImageScaleTraversable):
    """
    Resource Upload
    """
    name = schema.TextLine(
        title=u'Name',
        required=True,
    )

    email = schema.TextLine(
        title=u'E-mail',
        required=False,

    )

    church = schema.TextLine(
        title=u'Your church',
        required=False,
    )

    message = schema.Text(
        title=u'Message',
        required=True,
    )

    video = schema.Text(
        title=u'Video',
        required=False,
    )

    sound = schema.Text(
        title=u'Sound',
        required=False,
    )

    document = NamedBlobFile(
            title=_(u"Document"),
            description=_(u"Please attach a file"),
            required=False,
    )
    @invariant
    def addressInvariant(data):
        if data.email:
            if not re.match("[^@]+@[^@]+\.[^@]+", data.email):
                raise Invalid(_(u"Invalid email!"))

    form.widget(featured_resource=CheckBoxFieldWidget)
    featured_resource = schema.List(
           title=_(u"Set as Featured?"),
            value_type=schema.Choice(
	   values=[u"Featured"]),
	   required=False,
        )

#    video = RelationList(
#        title=u'Video',
#        default=[],
#        value_type=RelationChoice(
#            source=ObjPathSourceBinder(
#                path={'query': '/en/resources/videos'}
#            ),
#        ),
#        required=False
#    )

#    sound = RelationList(
#        title=u'Sound',
#        default=[],
#        value_type=RelationChoice(
#            source=ObjPathSourceBinder(
#                path={'query': '/en/resources/sounds'}
#            ),
#        ),
#        required=False
#    )

#    document = RelationList(
#        title=u'Document',
#        default=[],
#        value_type=RelationChoice(
#            source=ObjPathSourceBinder(
#                path={'query': '/en/resources/documents'}
#            ),
#        ),
#        required=False
#    )

    pass

alsoProvides(IResourceUpload, IFormFieldProvider)



@grok.subscribe(IResourceUpload, IObjectAddedEvent)
def _createObject(context, event):
    parent = context.aq_parent
    id = context.getId()
    object_Ids = []
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog.unrestrictedSearchResults(object_provides = IResourceUpload.__identifier__)
    for brain in brains:
        object_Ids.append(brain.id)
    
    last_name = str(idnormalizer.normalize(context.name))
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
    context.setTitle(context.name)

    #exclude from navigation code
    behavior = IExcludeFromNavigation(context)
    behavior.exclude_from_nav = True

    context.reindexObject()
    return


