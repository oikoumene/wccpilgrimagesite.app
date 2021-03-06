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
from zope.schema import ValidationError
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid
from zope.app.container.interfaces import IObjectAddedEvent
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form.interfaces import IAddForm, IEditForm


class InvalidEmailAddress(ValidationError):
    "Invalid email address"

def validateaddress(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True


# Interface class; used to define content-type schema.


class video_in_step(object):
    grok.implements(IContextSourceBinder)
    def __call__(self,context ):
        catalog = getToolByName(context,'portal_catalog')
        # brains = catalog(object_provides=IPilgrimageSteps.__identifier__)
        if context.portal_type == 'wccpilgrimagesite.app.video':
            path = '/'.join(context.aq_parent.aq_parent.aq_parent.getPhysicalPath())
            uid = context.aq_parent.aq_parent.Title()
        else:
            path = '/'.join(context.aq_parent.aq_parent.getPhysicalPath())
            uid = context.aq_parent.Title()
        brains = catalog.unrestrictedSearchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.pilgrimagesteps', review_state= 'published')
        items = []
        
        for brain in brains:
            if uid != brain.Title:
                items.append(SimpleTerm(brain.UID, title=brain.Title))
        return SimpleVocabulary(items)


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


# class IVideo(form.Schema, IImageScaleTraversable, utils.IVotingMixin, utils.IUserMixin):
class IVideo(form.Schema, IImageScaleTraversable):
    """
    Video
    """

    wcc_user = schema.Bool(
            title=u'WCC is an owner',
            required=True,
            default=False
        )

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
        required=False,
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
        description=u'Also show this on:',
        required=False,
        value_type=schema.Choice(source=video_in_step())
    )
    form.widget(featured_video_in_step=CheckBoxFieldWidget)
    featured_video_in_step = schema.List(
        title=u'As featured in pilgrimage steps',
        description=u'Select pilgrimage steps where this video will appear as a featured resource.',
        required=False,
        value_type=schema.Choice(source=featured_steps())
    )
    
    form.mode(IAddForm, uploader='hidden')
    form.mode(IEditForm, uploader='input')


    uploader = schema.TextLine(
        title=u"Name",
        required=False,
    )

    form.mode(IAddForm, email='hidden')
    form.mode(IEditForm, email='input')
    
    email = schema.TextLine(
        title=u'E-mail',
        required=False,
        constraint=validateaddress,

    )

    form.mode(votes_count='hidden')
    votes_count = schema.Int(
        title=u'Current votes count',
        required=False,
        default=0
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
    
    # @invariant
    # def resourcesInvariant(data):
    #     if not data.video_in_step:
    #         raise Invalid(_(u"No Pilgrimage Steps selected."))


    pass

alsoProvides(IVideo, IFormFieldProvider)

@form.error_message(field=IVideo['title'], error=RequiredMissing)
def titleOmittedErrorMessage(value):
    return u"No video name provided."

@form.error_message(field=IVideo['description'], error=RequiredMissing)
def descriptionOmittedErrorMessage(value):
    return u"No video description provided."

@form.error_message(field=IVideo['church'], error=RequiredMissing)
def churchOmittedErrorMessage(value):
    return u"No church provided."

@form.error_message(field=IVideo['url_youtube'], error=RequiredMissing)
def churchOmittedErrorMessage(value):
    return u"No Youtube URL provided."

# @form.default_value(field=IVideo['featured_video_in_step'])
# def value(self):
#     import pdb; pdb.set_trace()
#     return True


# @form.default_value(field=IVideo['featured_video_in_step'][''])
# def value(self):

#     return True


@grok.subscribe(IVideo, IObjectAddedEvent)
def _createObject(context, event):
    mailhost = getToolByName(context, 'MailHost')
    uploader = ''
    church = ''
    description = ''
    video = ''
    email = ''
    if context.uploader:
        uploader = context.uploader
    if context.church:
        church = context.church
    if context.description:
        description = context.description
    if context.url_youtube:
        video = context.url_youtube
    if context.email:
        email = context.email
    
    mSubj = "New Video Has Been Submitted"
    mFrom = 'pilgrimage@wcc-coe.org'
    mTo = 'afterfive2015@gmail.com, pilgrimage@wcc-coe.org'
    mBody = "A New Video Resource Has Been Submitted. Please see details below:\n"
    mBody += "\n"
    mBody += "Uploader: "+uploader+"\n"
    mBody += "Email: "+email+"\n"
    mBody += "Church: "+church+"\n"
    mBody += "Message: "+description+"\n"
    mBody += "Video: "+video+"\n"
    mBody += "\n"
    mBody += "To review the above pledge, visit:\n"
    mBody += "\n"
    mBody += context.absolute_url()+"\n"
    mBody += "\n"
    mBody += "To approve the post, click on the link below:\n"
    mBody += "\n"
    mBody += context.absolute_url()+"/content_status_modify?workflow_action=publish\n"
    mBody += "\n"
    mBody += "Thank you.\n\n"
    mBody += "----------\n"
    mBody += "WCC Pilgrimage\n"
    mBody += "pilgrimage@wcc-coe.org\n"
    mBody += "http://wccpilgrimage.org\n"
    try:
        mailhost.send(mBody, mto=mTo, mfrom=mFrom, subject=mSubj, immediate=True, charset='utf8', msg_type=None)
    except Exception, e:
        context.plone_utils.addPortalMessage(u'Unable to send email', 'info')
        return None

