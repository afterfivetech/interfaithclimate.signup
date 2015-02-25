from collective.grok import gs
from interfaithclimate.signup import MessageFactory as _

@gs.importstep(
    name=u'interfaithclimate.signup', 
    title=_('interfaithclimate.signup import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('interfaithclimate.signup.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
