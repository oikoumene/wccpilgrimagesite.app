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

featured = SimpleVocabulary(
[
    SimpleTerm(u'Featured', title=u'Featured'),
  
])

# Interface class; used to define content-type schema.

class ISound(form.Schema, IImageScaleTraversable):
    """
    Sound
    """

    title = schema.TextLine(
        title=u'Sound name',
        required=True,
    )

    description = schema.Text(
        title=u'Sound description',
        required=True,
    )

    church = schema.Text(
        title=u'church',
        required=True,
    )

    soundcloud_id = schema.TextLine(
        title=u'Soundcloud ID',
        required=True,
    )

    sound_in_step = schema.TextLine(
        title=u'In pilgrimage steps',
        description=u'Select pilgrimage steps where this sound will appear.',
        required=True,
    )

    featured_sound_in_step = schema.TextLine(
        title=u'As featured in pilgrimage steps',
        description=u'Select pilgrimage steps where this sound will appear as a featured resource.',
        required=True,
    )

    form.widget(featured_resource=CheckBoxFieldWidget)
    featured_resource = schema.List(
           title=u'Is this sound featured?',value_type=schema.Choice(vocabulary=featured)
        )

    # votes_count = schema.Int(
    #     title=u'Current votes count',
    #     required=False,
    #     default=0
    # )


    #sound_in_step = RelationList(
        #title=u'In pilgrimage steps',
        #description=u'Select pilgrimage steps where this sound will appear.',
        #default=[],
        #value_type=RelationChoice(
        #    source=ObjPathSourceBinder(
        #        path={'query': '/en/pilgrimage-steps'},
        #    ),
        #),
        #required=False,
    #)

    #featured_sound_in_step = RelationList(
        #title=u'As featured in pilgrimage steps',
        #description=u'Select pilgrimage steps where this sound will appear as a featured resource.',
        #default=[],
        #value_type=RelationChoice(
        #    source=ObjPathSourceBinder(
        #        path={'query': '/en/pilgrimage-steps'},
        #    ),
        #),
        #required=False,
    #)


    pass

alsoProvides(ISound, IFormFieldProvider)
