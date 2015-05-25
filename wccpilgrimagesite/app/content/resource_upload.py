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

from plone.dexterity.utils import createContentInContainer, createContent

from zope.schema import ValidationError
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid


class InvalidEmailAddress(ValidationError):
    "Invalid email address"

class InvalidYoutubeUrl(ValidationError):
    "Youtube link is not valid."

class InvalidSoundCloudId(ValidationError):
    "Please specify the Soundcloud track ID. If you don't know where to find it, please put 0 in the Audio field and include the URL of the sound file in the Message field."


def validateaddress(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True


def validatevideo(url):

    if bool(re.match(r'^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$',url)) == False:
        raise InvalidYoutubeUrl(url)
    else:
        return True

def validatesound(id):
    try: 
        int(id)
        return True
    except ValueError:
        raise InvalidSoundCloudId(id)


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
        constraint=validateaddress,

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
        constraint=validatevideo,
    )

    sound = schema.Text(
        title=u'Sound',
        required=False,
        constraint=validatesound
    )

    document = NamedBlobFile(
            title=_(u"Document"),
            description=_(u"Please attach a file"),
            required=False,
    )


    # form.widget(featured_resource=CheckBoxFieldWidget)
    # featured_resource = schema.List(
    #        title=_(u"Set as Featured?"),
    #         value_type=schema.Choice(
    #           values=[u"Featured"]),
    #         required=False,
    #     )

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
    
    
    #@invariant
    #def addressInvariant(data):
    #    if data.email:
    #        if not re.match("[^@]+@[^@]+\.[^@]+", data.email):
    #            raise Invalid(_(u"Invalid email!"))
    
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
    # behavior = IExcludeFromNavigation(context)
    # behavior.exclude_from_nav = True

    
    if context.video:
        item = createContentInContainer(parent,'wccpilgrimagesite.app.video', checkConstraints=False,title=context.name, )
        item.url_youtube = context.video
        item.description = context.message
        item.church = context.church

        item.reindexObject()
    
    if context.sound:
        item2 = createContentInContainer(parent,'wccpilgrimagesite.app.sound', checkConstraints=False,title=context.name)
        item2.soundcloud_id = context.sound
        item2.description = context.message
        item2.church = context.church
        item2.reindexObject()
        
    if context.document:
        item3 = createContentInContainer(parent,'wccpilgrimagesite.app.staticdocument', checkConstraints=False,title=context.name)
        item3.file = context.document
        item3.description = context.message
        item3.church = context.church
        item3.reindexObject()
    context.reindexObject()
    return


