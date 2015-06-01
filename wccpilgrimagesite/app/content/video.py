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
from wccpilgrimagesite.app import utils
from wccpilgrimagesite.app.content.pilgrimage_steps import IPilgrimageSteps
from Products.CMFCore.utils import getToolByName
import datetime
from zope.schema.interfaces import RequiredMissing


# Interface class; used to define content-type schema.


class featured_steps(object):
    grok.implements(IContextSourceBinder)
    def __call__(self,context ):
        catalog = getToolByName(context,'portal_catalog')
        # brains = catalog(object_provides=IPilgrimageSteps.__identifier__)
        if context.portal_type == 'wccpilgrimagesite.app.video':
            path = '/'.join(context.aq_parent.aq_parent.aq_parent.getPhysicalPath())
        else:
            path = '/'.join(context.aq_parent.aq_parent.getPhysicalPath())
        brains = catalog.unrestrictedSearchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.pilgrimagesteps', review_state= 'published')
        items = []
        for brain in brains:
            items.append(SimpleTerm(brain.UID, title=brain.Title))
        return SimpleVocabulary(items)


class IVideo(form.Schema, IImageScaleTraversable, utils.IVotingMixin, utils.IUserMixin):
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

    church = schema.Text(
        title=u'church',
        required=True,
    )

    url_youtube = schema.TextLine(
        title=u'Youtube URL',
        required=True,
    )

    # video_in_step = schema.Text(
    #     title=u'In pilgrimage steps',
    #     description=u'Select pilgrimage steps where this video will appear.',
    #     required=True,
    # )
    form.widget(video_in_step=CheckBoxFieldWidget)
    video_in_step = schema.List(
        title=u'In pilgrimage steps',
        description=u'Select pilgrimage steps where this video will appear.',
        required=True,
        value_type=schema.Choice(source=featured_steps())
    )
    form.widget(featured_video_in_step=CheckBoxFieldWidget)
    featured_video_in_step = schema.List(
        title=u'As featured in pilgrimage steps',
        description=u'Select pilgrimage steps where this video will appear as a featured resource.',
        required=False,
        value_type=schema.Choice(source=featured_steps())
    )

    # form.widget(featured_resource=CheckBoxFieldWidget)
    # featured_resource = schema.List(
    #        title=u'Is this video featured?',value_type=schema.Choice(vocabulary=featured)
    #     )

    # votes_count = schema.Int(
    #     title=u'Current votes count',
    #     required=False,
    #     default=0
    # )






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
    
    @invariant
    def resourcesInvariant(data):
        if not data.video_in_step:
            raise Invalid(_(u"No Pilgrimage Steps selected."))


    pass

alsoProvides(IVideo, IFormFieldProvider)

@form.error_message(field=IVideo['title'], error=RequiredMissing)
def titleOmittedErrorMessage(value):
    return u"No name provided."

@form.error_message(field=IVideo['description'], error=RequiredMissing)
def descriptionOmittedErrorMessage(value):
    return u"No description provided."

@form.error_message(field=IVideo['church'], error=RequiredMissing)
def churchOmittedErrorMessage(value):
    return u"No church provided."

@form.error_message(field=IVideo['url_youtube'], error=RequiredMissing)
def youtubeURLOmittedErrorMessage(value):
    return u"No Youtube URL provided."


