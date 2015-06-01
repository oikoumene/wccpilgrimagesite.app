import json

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#import plone.api
from Products.CMFCore.utils import getToolByName
from wccpilgrimagesite.app.content.video import IVideo
from zope.component.hooks import getSite
import urlparse


#from wccpilgrimagesite.app import utils, content

def is_number(s):
    try:
        float(s)
        return True
    except Exception:
        return False
        

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
    
class ResourceVideosPaginate(ApiView):
    
    def __call__(self):
        html = ''
        show_see_more = True
        if self.request:
            if self.request.form:
                form = self.request.form
                path = form.get('path')[:-1]
                step = form.get('step')
                startPage = 0
                if is_number(step):
                    startPage = int(step)
                portal = getSite()
                catalog = getToolByName(portal, 'portal_catalog')
                resources = catalog.unrestrictedSearchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.video',sort_on='Date',
                                                sort_order='reverse',review_state= 'published')
                steps = catalog.unrestrictedSearchResults(object_provides=IVideo.__identifier__,sort_on='Date',sort_order='reverse',review_state= 'published')
                videos_resources = []
                videos_steps = []
                for brain in resources:
                    obj = brain._unrestrictedGetObject()
                    data_resources = {'title': obj.title,
                                'description':obj.description,
                                'url_youtube': self.url_youtube_embedded(obj.url_youtube),
                                'uid': brain.UID,
                                'votes_count': obj.votes_count,
                                'created': brain.created,
                                'wcc_user':obj.wcc_user}
                    videos_resources.append(data_resources)
                for brain in steps:
                    obj = brain._unrestrictedGetObject()
                    if obj.video_in_step:
                        if context.aq_parent.UID() in obj.video_in_step:
                            data_steps = {'title': obj.title,
                                'description':obj.description,
                                'url_youtube': self.url_youtube_embedded(obj.url_youtube),
                                'uid': brain.UID,
                                'votes_count': obj.votes_count,
                                'created': brain.created,
                                'wcc_user':obj.wcc_user}
                        
                            videos_steps.append(data_steps)
        
                for video in videos_resources:
                    if video not in videos_steps:
                        videos_steps.append(video)
                paginated_videos = []
                if len(videos_steps) > 3:
                    
                    paginated_videos = videos_steps[startPage*3:(startPage*3)+3]
                
                for pv in paginated_videos:
                    html += "<li class='animated fadeInRight'>"
                    html += "<h3>"+pv['title']+"</h3>"
                    html += "<div>"
                    html += "<a class='video-links fancybox.iframe' href="+pv['url_youtube']+">"
                    html += "<img src="+self.url_youtube_bg_img(pv['url_youtube'])+"></a>"
                    html += "</div>"
                    html += "<ul class='no-bullet icons-box'>"
                    if pv['wcc_user']:
                        html += "<li class='user-icon wcc-user'>"
                        html += "<img src='++theme++wccpilgrimagesite.theme/images/wcc-user-icon.png' alt='' />"
                        html += "<span class='access'>User</span>"
                        html += "</li>"
                    else:
                        html += "<li class='user-icon unknown-user'>"
                        html += "<i class='fa fa-user'></i>"
                        html += "<span class='access'>User</span>"
                        html += "</li>"
                    html += "<li class='heart-icon'>"
                    html += "<a data-votable="+pv['uid']+"><i class='fa fa-heart'></i></a>"
                    html += "</li>"
                    html += "<li class='heart-count' data-votes-count="+pv['uid']+">"+str(pv['votes_count'])+"</li>"
                    html += "</ul>"
                    html += "<p>"+pv['description']+"</p>"
                    html += "</li>"
                
                if len(videos_steps)-1 >= startPage*3 and len(videos_steps)-1 <= (startPage*3)+2:
                    show_see_more = False
        return self._response(response={'html':html, 'show_see_more':show_see_more})
                    
                    
    def url_youtube_bg_img(self, url=None):
        return 'http://img.youtube.com/vi/{hash}/hqdefault.jpg'.format(hash=self._hash_from_url_youtube(url))
    
    def url_youtube_embedded(self, url=None):
        return 'http://www.youtube.com/embed/{hash}'.format(hash=self._hash_from_url_youtube(url))
    
    def _hash_from_url_youtube(self, url=None):
        # Reference: http://stackoverflow.com/a/7936523/545435

        query = urlparse.urlparse(url)
        if query.hostname == 'youtu.be':
            return query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                p = urlparse.parse_qs(query.query)
                return p['v'][0]
            if query.path[:7] == '/embed/':
                return query.path.split('/')[2]
            if query.path[:3] == '/v/':
                return query.path.split('/')[2]
        return ''
                
                
                    

