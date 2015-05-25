from five import grok
from plone.directives import dexterity, form
from Products.CMFCore.interfaces import IContentish
import plone.api
import json

grok.templatedir('templates')

class api_view(grok.View):
    grok.context(IContentish)
    grok.require('zope2.View')
    grok.name('api+upvote')
    
    def __call__(self):
        id = self.request.form.get('id')
        if not id:
            return self._response(status_code=400)

        obj = plone.api.content.get(UID=id)
        if not obj:
            return self._response(status_code=400)

        obj.votes_count += 1

        return self._response()
    
    def _response(self, response={}, status_code=200, status_message=''):
        view_response = self.request.response
        view_response.setHeader('Content-type', 'application/json')
        view_response.setStatus(status_code, status_message)
        view_response.setBody(json.dumps(response), lock=True)

        return view_response
    