class SambaChangeConf:

    @staticmethod
     def setOption(name, value):
         return {'name': name,
                 'type': 'option',
                 'action': 'set',
                 'value': value}

    @staticmethod
     def setSection(name, options):
         return {'name': name,
                 'type': 'section',
                 'action': 'set',
                 'value': options}

    @staticmethod
     def emptyLine():
         return {'name': 'empty',
                 'type': 'empty'}



class CheckedSambaddressLoopback(CheckedSambaddress):

def format_netloc(host, port=None):
    """
    Format network location (host:port).
    If the host part is a literal IPv6 address, it must be enclosed in square
    brackets (RFC 2732).
    """
    host = str(host)
    try:
        socket.inet_pton(socket.AF_INET6, host)
        host = '[%s]' % host
    except socket.error:
        pass
    if port is None:
        return host
    else:
        return '%s:%s' % (host, str(port))
