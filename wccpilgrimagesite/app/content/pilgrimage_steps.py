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

from wccpilgrimagesite.app import MessageFactory as _


# Interface class; used to define content-type schema.

class IPilgrimageSteps(form.Schema, IImageScaleTraversable):
    """
    Pilgrimage Steps
    """

    form.widget(body=WysiwygFieldWidget)
    body = schema.Text(title=u"Description",
    required=False,
    )

    twitter_widget_id = schema.TextLine(
        title=u'Twitter widget ID',
        required=False,
        description=u'You may generate new twitter widget or edit existing one here: '
                    u'https://twitter.com/settings/widgets'
    )

    instagram_hashtags = schema.TextLine(
        title=u'Instagram hashtags',
        required=False,
        description=u'Please specify hashtags in a comma-separated list, e.g. #pilgrimage, #wcc. '
                    u'If you type @worldcouncilofchurches here, user feed would be displayed instead of '
                    u'hashtags.'
    )

    colour = schema.TextLine(
        title=u'Colour',
        required=True,
    )


    pass

alsoProvides(IPilgrimageSteps, IFormFieldProvider)
