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

class IUserComment(form.Schema, IImageScaleTraversable):
    """
    User Comment
    """

    title = schema.TextLine(
        title=u'Name',
        required=True,
    )

    email = schema.TextLine(
        title=u'E-mail',
        required=True,
    )

    message = schema.Text(
        title=u'Message',
        required=False,
    )

    datetime_added = schema.Datetime(
        title=u'Datetime added',
        required=True,
    )

    image = NamedBlobImage(
        title=u'Image',
        required=False,
    )

#    comment_in_steps = RelationList(
#        title=u'Pilgrimage step',
#        default=[],
#        value_type=RelationChoice(
#            source=ObjPathSourceBinder(
#                path={'query': '/en/pilgrimage-steps'},
#            ),
#        ),
#        required=False,
#    ) 

    pass

alsoProvides(IUserComment, IFormFieldProvider)
