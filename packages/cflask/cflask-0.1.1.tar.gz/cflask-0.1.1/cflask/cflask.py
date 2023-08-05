'''
Brief:
    File for cFlask, which is a lite wrapper around flask that supports a (very)
        simple framework for API versioning

License:
    MIT License

Author(s):
    Charles Machalow
'''

import logging
import threading
from flask import Flask

DEFAULT = 'Default'
LOGGER = logging.getLogger(__name__)
URL_PREFIX = 'handleV'

class cFlask(Flask):
    '''
    cFlask allows a simple versioning schema for APIs
    '''
    def __init__(self, *args, **kwargs):
        '''
        allows all normal Flask args/kwargs. Adds in a urlPrefix kwarg to overload the
            URL_PREFIX used as the prefix to the individual version commands.
        '''
        if 'urlPrefix' in kwargs:
            self._urlPrefix = kwargs['urlPrefix']
            del kwargs['urlPrefix']
        else:
            self._urlPrefix = URL_PREFIX

        Flask.__init__(self, *args, **kwargs)

        # allow the user's naming to allow default routing still
        setattr(self, self._urlPrefix + DEFAULT, self.handleVDefault)

        # add full path router
        self.add_url_rule('/<path:fullPath>', view_func=self.fullPathRouter)
        self.add_url_rule('/', view_func=self.handleVDefault, defaults={'fullPath' : ''})

    def _isValidVersion(self, ver):
        '''
        returns True if this version is implemented
        '''
        return hasattr(self, self._urlPrefix + str(ver))

    def fullPathRouter(self, fullPath):
        '''
        called when any request comes in. The path will be used to route the command to
            the correct version handler. If the handler cannot be found, calls handleVDefault(fullPath)
        '''
        version = fullPath.split('/')[0]
        if version.isdigit():
            if self._isValidVersion(version):
                remainingPath = '/'.join(fullPath.split('/')[1:])
                funcName = self._urlPrefix + version

                LOGGER.info("Sending the remainingPath (%s) to %s()" % (remainingPath, funcName))
                retVal = getattr(self, funcName)(remainingPath)
                if retVal is not False: # if the version handler gives False, return the default handler
                    return retVal
                else:
                    LOGGER.info("%s() returned False... passing to default handler" % funcName)

        LOGGER.info("Sending the fullPath (%s) to handleVDefault()" % fullPath)
        return self.handleVDefault(fullPath)

    def handleVDefault(self, fullPath):
        '''
        default handler (when version could not be found). Feel free to overload.
        '''
        return 'Page Not Found', 404

class _ExampleCFlask(cFlask):
    '''
    example of a simple cFlask server.
    '''
    def handleV1(self, info):
        '''
        handles v1. If the passed info is "False" return False.
            Returning False will lead to the default handler getting called.
        '''
        if info == 'False':
            return False

        return 'V1: %s' % info

    def handleV2(self, info):
        '''
        handles v2
        '''
        return 'V2: %s' % info

    def handleVDefault(self, fullPath):
        '''
        handles unversioned / default requests
        '''
        return 'VDefault: %s' % fullPath

if __name__ == '__main__':
    c = _ExampleCFlask(__name__)
    t = threading.Thread(target=c.run)
    t.setDaemon(True)
    t.start()