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
