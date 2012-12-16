class Base(object):
    """ Base class for resources

    Derived classes must define:
        pattern - compiled regex used to match URLs
        url - the URL of the resource
        __init__() - takes the matched URL groups as arguments
        found - set True by __init__ when found
        methods - method -> (input reader, perform, output writer) lookup
    """
    def authenticate(self):
        return None

    def authorize(self):
        return None

    def find(self):
        return True

    def respond(self, env, start_response):
        m = env['REQUEST_METHOD']
        if m in self.methods:
            rin, perform, wout = self.methods[m]

            inlen = env.get('CONTENT_LENGTH', 0)
            if rin:
                intype = env.get('CONTENT_TYPE', None)
                if intype not in rin:
                    start_response('415 Unsupported Media Type', [('Content-Type', 'text/plain')])
                    return ['Supported media types for {0} {1}: {2}'.format(m, self.url, ', '.join(rin.keys()))]
                rin = rin[intype]
            else:
                if inlen > 0:
                    start_response('413 Request Entity Too Large', [('Content-Type', 'text/plain')])
                    return ['No entity expected in {0} {1} request'.format(m, self.url)]

            if wout:
                outtype = env.get('HTTP_ACCEPT')
                if outtype not in wout:
                    start_response('406 Not Acceptable', [('Content-Type', 'text/plain')])
                    return ['Supported media types for {0} {1}: {2}'.format(m, self.url, ', '.join(wout.keys()))]
                wout = wout[outtype]

            success, location, data = perform(self, env, rin, wout)
            if success:
                if data:
                    content_type = ('Content-Type', outtype)
                    if location:
                        start_response('201 Created', [content_type, ('Location', location)])
                    else:
                        start_response('200 OK', [content_type])
                    return [data]
                else:
                    start_response('204 No Content', [])
                    return []
            else:
                start_response('400 Bad Request', [('Content-Type', 'text/plain')])
                return [data]
        else:
            start_response('405 Method Not Allowed', [('Content-Type', 'text/plain')])
            return ['Supported methods for {0}: {1}'.format(self.url, ', '.join(self.methods.keys()))]


