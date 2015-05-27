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
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from wccpilgrimagesite.app import MessageFactory as _


from wccpilgrimagesite.app.content.pilgrimage_steps import IPilgrimageSteps
from Products.CMFCore.utils import getToolByName
import datetime
from wccpilgrimagesite.app import utils


# Interface class; used to define content-type schema.


class featured_steps(object):
    grok.implements(IContextSourceBinder)
    def __call__(self,context ):
        catalog = getToolByName(context,'portal_catalog')
        brains = catalog(object_provides=IPilgrimageSteps.__identifier__)
        items = []
        
        for brain in brains:
            items.append(SimpleTerm(brain.UID, title=brain.Title))
        return SimpleVocabulary(items)

class IStaticDocument(form.Schema, IImageScaleTraversable, utils.IVotingMixin):
    """
    Static Document
    """

    title = schema.TextLine(
        title=u'Document name',
        required=True,
    )

    description = schema.Text(
        title=u'Document description',
        required=True,
    )

    church = schema.Text(
        title=u'Church',
        required=True,
    )


    file = NamedBlobFile(
        title=u'File',
        required=True,
    )

    file_thumb = NamedBlobFile(
        title=u'File thumb',
        description=u'Thumbnail of the file (if PDF) - will be generated automatically.',
        required=False,
    )

    # doc_in_step = schema.Text(
    #     title=u'In pilgrimage steps',
    #     description=u'Select pilgrimage steps where this document will appear.',
    #     required=True,
    # )
    form.widget(doc_in_step=CheckBoxFieldWidget)
    doc_in_step = schema.List(
        title=u'In pilgrimage steps',
        description=u'Select pilgrimage steps where this document will appear.',
        required=True,
        value_type=schema.Choice(source=featured_steps())
    )

    form.widget(featured_doc_in_step=CheckBoxFieldWidget)
    featured_doc_in_step = schema.List(
        title=u'As featured in pilgrimage steps',
        description=u'Select pilgrimage steps where this document will appear as a featured resource.',
        required=False,
        value_type=schema.Choice(source=featured_steps())
    )

    # featured_doc_in_step = schema.Text(
    #     title=u'As featured in pilgrimage steps',
    #     description=u'Select pilgrimage steps where this document will appear as a featured resource.',
    #     required=True,
    # )

    # form.widget(featured_resource=CheckBoxFieldWidget)
    # featured_resource = schema.List(
    #        title=u'Is this document featured?',value_type=schema.Choice(vocabulary=featured)
    #     )

    # votes_count = schema.Int(
    #     title=u'Current votes count',
    #     required=False,
    #     default=0
    # )


    #doc_in_step = RelationList(
        #title=u'In pilgrimage steps',
        #description=u'Select pilgrimage steps where this document will appear.',
        #default=[],
        #value_type=RelationChoice(
        #    source=ObjPathSourceBinder(
        #        path={'query': '/en/pilgrimage-steps'},
        #    ),
        #),
        #required=False,
    #)

    #featured_doc_in_step = RelationList(
        #title=u'As featured in pilgrimage steps',
        #description=u'Select pilgrimage steps where this document will appear as a featured resource.',
        #default=[],
        #value_type=RelationChoice(
        #    source=ObjPathSourceBinder(
        #        path={'query': '/en/pilgrimage-steps'},
        #    ),
        #),
        #required=False,
    #)


    pass

alsoProvides(IStaticDocument, IFormFieldProvider)
