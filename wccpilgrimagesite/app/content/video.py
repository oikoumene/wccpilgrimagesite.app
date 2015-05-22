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


# Interface class; used to define content-type schema.

class IVideo(form.Schema, IImageScaleTraversable):
    """
    Video
    """

    title = schema.TextLine(
        title=u'Video name',
        required=True,
    )

    description = schema.Text(
        title=u'Video description',
        required=True,
    )

    url_youtube = schema.TextLine(
        title=u'Youtube URL',
        required=True,
    )

    video_in_step = schema.Text(
        title=u'In pilgrimage steps',
        description=u'Select pilgrimage steps where this video will appear.',
        required=True,
    )

    featured_video_in_step = schema.Text(
        title=u'As featured in pilgrimage steps',
        description=u'Select pilgrimage steps where this video will appear as a featured resource.',
        required=True,
    )

    form.widget(featured_resource=CheckBoxFieldWidget)
    featured_resource = schema.List(
           title=_(u"Set as Featured?"),
            value_type=schema.Choice(
	   values=[u"Featured"]),
	   required=False,
        )

    #video_in_step = RelationList(
        #title=u'In pilgrimage steps',
        #description=u'Select pilgrimage steps where this video will appear.',
        #default=[],
        #value_type=RelationChoice(
        #    source=ObjPathSourceBinder(
        #        path={'query': '/en/pilgrimage-steps'},
        #    ),
        #),
        #required=False,
    #)

    #featured_video_in_step = RelationList(
        #title=u'As featured in pilgrimage steps',
        #description=u'Select pilgrimage steps where this video will appear as a featured resource.',
        #default=[],
        #value_type=RelationChoice(
        #    source=ObjPathSourceBinder(
        #        path={'query': '/en/pilgrimage-steps'},
        #    ),
        #),
        #required=False,
    #)


    pass

alsoProvides(IVideo, IFormFieldProvider)
