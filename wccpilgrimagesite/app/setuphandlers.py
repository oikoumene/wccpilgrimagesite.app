from collective.grok import gs
from wccpilgrimagesite.app import MessageFactory as _

@gs.importstep(
    name=u'wccpilgrimagesite.app', 
    title=_('wccpilgrimagesite.app import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('wccpilgrimagesite.app.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
