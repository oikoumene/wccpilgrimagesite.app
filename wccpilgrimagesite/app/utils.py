import re
import base64
import time
import hashlib

#from plone import api
from plone.supermodel import model
from plone.uuid.interfaces import IUUID
from OFS.interfaces import IOrderedContainer
from Acquisition import aq_inner
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zope import schema
from zc.relation.interfaces import ICatalog
from zope.component.hooks import getSite
from plone.directives import dexterity, form

class IVotingMixin(form.Schema):
    form.mode(votes_count='hidden')
    votes_count = schema.Int(
        title=u'Current votes count',
        required=False,
        default=0
    )

class VotingMixin(object):

    def upvote1(self):
        self.votes_count += 1


