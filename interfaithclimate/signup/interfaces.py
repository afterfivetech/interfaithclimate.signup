from zope.interface import Interface
from quintagroup.z3cform.captcha import Captcha
from interfaithclimate.signup import MessageFactory as _

class IProductSpecific(Interface):
    pass


class ICaptchaSchema(Interface):
    captcha = Captcha(
        title=_(u'Type the code'),
        description=_(u'Type the code from the picture shown below.'))
