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
from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.i18n.normalizer import idnormalizer
import datetime


from zope.interface import invariant, Invalid
import re
# Interface class; used to define content-type schema.
from wccpilgrimagesite.app import utils

from zope.schema import ValidationError
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid
from zope.schema.interfaces import RequiredMissing

class InvalidEmailAddress(ValidationError):
    "Invalid email address"

def validateaddress(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True

class IUserComment(form.Schema, IImageScaleTraversable, utils.IVotingMixin):
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
        constraint=validateaddress,
    )

    message = schema.Text(
        title=u'Message',
        required=True,
    )

    # datetime_added = schema.Datetime(
    #     title=u'Datetime added',
    #     required=True,
    # )

    image = NamedBlobImage(
        title=u'Image',
        required=False,
    )

    # votes_count = schema.Int(
    #     title=u'Current votes count',
    #     required=False,
    #     default=0
    # )

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

    # @invariant
    # def addressInvariant(data):
    #     if not re.match("[^@]+@[^@]+\.[^@]+", data.email):
    #         raise Invalid(_(u"Invalid email!"))
    # pass

alsoProvides(IUserComment, IFormFieldProvider)



@grok.subscribe(IUserComment, IObjectAddedEvent)
def _createObject(context, event):
    parent = context.aq_parent
    id = context.getId()
    object_Ids = []
    catalog = getToolByName(context, 'portal_catalog')
    path = '/'.join(parent.getPhysicalPath())
    brains = catalog.unrestrictedSearchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.usercomment')
    for brain in brains:
        object_Ids.append(brain.id)
    
    temp_new_id = str(idnormalizer.normalize(context.title))
    new_id = temp_new_id.replace("-","")
    test = ''
    if new_id in object_Ids:
        test = filter(lambda name: new_id in name, object_Ids)
        if len(test) > 1:
            test = filter(lambda name: new_id+'-' in name, object_Ids)
        if '-' not in (max(test)):
            new_id = new_id + '-1'
        if '-' in (max(test)):
            new_id = new_id +'-' +str(int(max(test).split('-')[-1])+1) 

    parent.manage_renameObject(id, new_id )
    context.setTitle(context.title)

    #exclude from navigation code
    # behavior = IExcludeFromNavigation(context)
    # behavior.exclude_from_nav = True

    context.reindexObject()
    return

# @form.default_value(field=IUserComment['datetime_added'])
# def currentDate(self):
#     return datetime.datetime.today()


@form.error_message(field=IUserComment['title'], error=RequiredMissing)
def nameOmittedErrorMessage(value):
    return u"No name provided."

@form.error_message(field=IUserComment['message'], error=RequiredMissing)
def nameOmittedErrorMessage(value):
    return u"No message provided."

@form.error_message(field=IUserComment['email'], error=RequiredMissing)
def nameOmittedErrorMessage(value):
    return u"No email provided."