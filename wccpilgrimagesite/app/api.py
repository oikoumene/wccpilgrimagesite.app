import json

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#import plone.api


#from wccpilgrimagesite.app import utils, content


class ApiView(BrowserView):

    def _response(self, response={}, status_code=200, status_message=''):
        view_response = self.request.response
        view_response.setHeader('Content-type', 'application/json')
        view_response.setStatus(status_code, status_message)
        view_response.setBody(json.dumps(response), lock=True)

        return view_response


class ApiUpvoteView(ApiView):

    def __call__(self):
        id = self.request.form.get('id')
        if not id:
            return self._response(status_code=400)

        obj = plone.api.content.get(UID=id)
        if not obj:
            return self._response(status_code=400)

        obj.upvote1()

        return self._response()
