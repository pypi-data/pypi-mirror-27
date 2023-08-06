#the smp server implementation
import socket
try:
    import ujson as json
except ImportError:
    import json
try:
    import ustruct as struct
except ImportError:
    import struct

#from micropython import const

#smp methods
SMP_METHOD_GET = (1)
SMP_METHOD_POST = (2)
SMP_METHOD_PUT = (3)
SMP_METHOD_DELETE = (4)
#SMP message types
SMP_TYPE_CONFIRMABLE = (0)
SMP_TYPE_NON_CONFIRMABLE = (1)
SMP_TYPE_ACKNOWLEDGEMENT = (2)
SMP_TYPE_RESET = (3)
#smp content types
SMP_CONTENTFORMAT_TEXT_PLAIN = (0)
SMP_CONTENTFORMAT_APPLICATION_LINKFORMAT = (40)
SMP_CONTENTFORMAT_APPLICATION_XML = (41)
SMP_CONTENTFORMAT_APPLICATION_OCTET_STREAM = (42)
SMP_CONTENTFORMAT_APPLICATION_EXI = (47)
SMP_CONTENTFORMAT_APPLICATION_JSON = (50)
#SMP option value types
SMP_OPTION_TYPE_EMPTY = (0)
SMP_OPTION_TYPE_OPAQUE = (1)
SMP_OPTION_TYPE_UINT = (2)
SMP_OPTION_TYPE_STRING = (3)
#SMP options
SMP_OPTION_IF_MATCH = (1)
SMP_OPTION_URI_HOST = (3)
SMP_OPTION_ETAG = (4)
SMP_OPTION_IF_NONE_MATCH = (5)
SMP_OPTION_URI_PORT = (7)
SMP_OPTION_LOCATION_PATH = (8)
SMP_OPTION_URI_PATH = (11)
SMP_OPTION_CONTENT_FORMAT = (12)
SMP_OPTION_MAX_AGE = (14)
SMP_OPTION_URI_QUERY = (15)
SMP_OPTION_ACCEPT = (17)
SMP_OPTION_LOCATION_QUERY = (20)
SMP_OPTION_PROXY_URI = (35)
SMP_OPTION_PROXY_SCHEME = (39)
#SMP options registry
smpOptionsRegistry = {
        SMP_OPTION_URI_HOST: {
            'name': 'Uri-Host',
            'type': SMP_OPTION_TYPE_STRING,
            'min_size': 1,
            'max_size': 255,
            'default': None,
            'repeatable': False
        },
        SMP_OPTION_URI_PORT: {
            'name': 'Uri-Port',
            'type': SMP_OPTION_TYPE_UINT,
            'min_size': 0,
            'max_size': 2,
            'default': None,
            'repeatable': False
        },
        SMP_OPTION_URI_PATH: {
            'name': 'Uri-Path',
            'type': SMP_OPTION_TYPE_STRING,
            'min_size': 0,
            'max_size': 255,
            'default': None,
            'repeatable': True
        },
        SMP_OPTION_CONTENT_FORMAT: {
            'name': 'Content-Format',
            'type': SMP_OPTION_TYPE_UINT,
            'min_size': 0,
            'max_size': 2,
            'default': None,
            'repeatable': False
        },
        SMP_OPTION_URI_QUERY: {
            'name': 'Uri-Query',
            'type': SMP_OPTION_TYPE_STRING,
            'min_size': 0,
            'max_size': 255,
            'default': None,
            'repeatable': True
        },
        SMP_OPTION_ACCEPT: {
            'name': 'Accept',
            'type': SMP_OPTION_TYPE_UINT,
            'min_size': 0,
            'max_size': 2,
            'default': None,
            'repeatable': False
        }
    }
#SMP response codes
SMP_SUCCESS_CREATED = (65) #2.01
SMP_SUCCESS_DELETED = (66) #2.02
SMP_SUCCESS_VALID = (67) #2.03
SMP_SUCCESS_CHANGED = (68) #2.04
SMP_SUCCESS_CONTENT = (69) #2.05
SMP_CLIENT_ERROR_BAD_REQUEST = (128) #4.00
SMP_CLIENT_ERROR_UNAUTHORIZED = (129) #4.01
SMP_CLIENT_ERROR_BAD_OPTION = (130) #4.02
SMP_CLIENT_ERROR_FORBIDDEN = (131) #4.03
SMP_CLIENT_ERROR_NOT_FOUND = (132) #4.04
SMP_CLIENT_ERROR_METHOD_NOT_ALLOWED = (133) #4.05
SMP_CLIENT_ERROR_NOT_ACCEPTABLE = (134) #4.06
SMP_CLIENT_ERROR_PRECONDITION_FAILED = (140) #4.12
SMP_CLIENT_ERROR_REQUEST_ENTITY_TOO_LARGE = (141) #4.13
SMP_CLIENT_ERROR_UNSUPPORTED_CONTENT_FORMAT = (143) #4.15
SMP_SERVER_ERROR_INTERNAL_SERVER_ERROR = (160) #5.00
SMP_SERVER_ERROR_NOT_IMPLEMENTED = (161) #5.01
SMP_SERVER_ERROR_BAD_GATEWAY = (162) #5.02
SMP_SERVER_ERROR_SERVICE_UNAVAILABLE = (163) #5.03
SMP_SERVER_ERROR_GATEWAY_TIMEOUT = (164) #5.04
SMP_SERVER_ERROR_PROXYING_NOT_SUPPORTED = (165) #5.05
#SMP message formats
SMP_PAYLOAD_MARKER = (0xFF)
#SMP errors
class SmpMessageFormatError(Exception):
    pass

class SmpVersionError(Exception):
    pass

class SmpNotFoundError(Exception):
    pass

class SmpContentFormatError(Exception):
    pass

class SmpBadOptionError(Exception):
    pass
#CoAP Resource
class SmpResource(object):
    def __init__(self, path, server, handle_get, handle_put):
        self.title = None
        self.path = path
        self.server = server
        self.rt = None
        self.if_ = None
        self.ct = None
        self.children = []
        #handler functions - post and delete are not implemented
        self.handle_get = handle_get
        self.handle_put = handle_put

    def addChild(self, child):
        child.path = self.path + '/' + child.path
        self.children.append(child)
        self.server.addResource(child)

    def removeChild(self, child):
        self.children.remove(child)
        self.server.deleteResource(child)

    def getChildren(self, child):
        return self.children

    def removeChildren(self):
        for r in self.children:
            self.server.deleteResource(r.path)
        self.children = []

    def get(self, *args, **kwargs):
        try:
            return SmpPayload(*self.handle_get(*args, **kwargs))
        except TypeError:
            #no handler function was passed
            return SmpPayload('Not Implemented', 0)

    def put(self, *args, **kwargs):
        try:
            return SmpPayload(*self.handle_put(*args, **kwargs))
        except TypeError:
            #no handler function was passed
            return SmpPayload('Not Implemented', 0)

class WellKnownCore(SmpResource):
    def __init__(self, server):
        super().__init__('.well-known/core', server, None, None)

    def get(self, *args, **kwargs):
        return SmpPayload(self.server.getResourcesInCoRELinkFormat(), 40)

class SmpOption(object):
    def __init__(self, number, value):
        self.number = number
        self.value = value

        if not self.number in smpOptionsRegistry:
            raise SmpUnknownOptionError()

    def length(self):
        if self.type() == SMP_OPTION_TYPE_EMPTY:
            return 0
        elif self.type() == SMP_OPTION_TYPE_OPAQUE:
            return len(self.value)
        elif self.type() == SMP_OPTION_TYPE_UINT:
            #calc minimum number of bytes needed to represent this integer
            length = 0
            int_val = int(self.value)
            while int_val:
                int_val >>= 8
                length += 1
            if length > 4:
                #unzulässig
                pass
            return length
        elif self.type() == SMP_OPTION_TYPE_STRING:
            return len(bytes(self.value, 'utf-8'))

    def type(self):
        return smpOptionsRegistry[self.number]['type']

    def is_critical(self):
        return bool(self.value & 1)

    def is_unsafe(self):
        return bool(self.number & 2)

    def __lt__(self, other):
        #overload '<' operator to sort options
        return self.number < other.number

#CoAP payload
class SmpPayload(object):
    def __init__(self, payload, content_format):
        self.data = payload
        self.content_format = content_format

#CoAP Message
class SmpMessage(object):
    @classmethod
    def deserialize(cls, dgram):
        msg = cls()
        datagram = dgram
        dgram_len = len(datagram)
        pos = 0
        running_delta = 0
        datagram_deserialization_complete = False

        if dgram_len < 12:
            #Header must have at least 4 bytes
            raise SmpMessageFormatError('CoAP message has a length of less than 12 bytes')
        elif dgram_len >= 12:
            header = struct.unpack_from('!BBH4s4s', datagram, pos)
            pos += 12

            msg.ver = (header[0] & 0b00001100) >> 2
            #if msg.ver != 1:
            #    raise SmpVersionError('smp version is not 1')
            msg.type = (header[0] & 0b00000011) >> 0
            msg.tkl = (header[0] & 0b11110000) >> 4

            msg.code = header[1]
            if msg.code == 0:
                raise SmpMessageFormatError('message of type Empty has more than 4 bytes')
            msg.msgid = header[2]
            msg.addr = header[3]
            msg.random = header[4]

            if msg.tkl > 0:
                fmt = '!{0}s'.format(msg.tkl)
                msg.token = struct.unpack_from(fmt, datagram, pos)[0]
                pos += msg.tkl

            while not datagram_deserialization_complete:
                try:
                    next_byte = struct.unpack_from('!B', datagram, pos)[0]
                    pos += 1
                except:
                    #print('Ende erreicht')
                    datagram_deserialization_complete = True
                    break

                if next_byte != SMP_PAYLOAD_MARKER:
                    option_header = next_byte
                    option_delta = (option_header & 0xF0) >> 4
                    option_length = option_header & 0x0F

                    if option_delta == 13:
                        delta = struct.unpack_from('!B', datagram, pos)[0] + 13
                        pos += 1
                    elif option_delta == 14:
                        delta = struct.unpack_from('!B', datagram, pos)[0] + 269
                        pos += 1
                    elif option_delta == 15:
                        raise SmpMessageFormatError('option number must not be 15')
                    else:
                        delta = option_delta

                    option_number = delta + running_delta
                    running_delta += delta

                    if option_length == 13:
                        length = struct.unpack_from('!B', datagram, pos)[0] + 13
                        pos += 1
                    elif option_length == 14:
                        length = struct.unpack_from('!B', datagram, pos)[0] + 269
                        pos += 1
                    elif option_length == 15:
                        raise SmpMessageFormatError('option length must not be 15')
                    else:
                        length = option_length

                    fmt = '!{0}s'.format(length)
                    option_value = struct.unpack_from(fmt, datagram, pos)[0]
                    pos += length

                    msg.options.append(SmpOption(option_number, option_value))
                else:
                    try:
                        fmt = '!{0}s'.format(dgram_len - pos)
                        msg.payload = struct.unpack_from(fmt, datagram, pos)[0]
                        datagram_deserialization_complete = True
                    except:
                        raise SmpMessageFormatError('Payload too short')

        return msg

    def serialize(self):
        values = []
        self.tkl = 0
        if self.token:
            self.tkl = len(self.token)

        fmt = '!BBH4s4s'
        values.append(self.type | (self.ver << 2) | (self.tkl << 4))
        values.append(self.code)
        values.append(self.msgid)
        values.append(self.addr)
        values.append(self.random)

        if self.token:
            fmt += '{0}s'.format(self.tkl)
            values.append(self.token)
        if self.options:
            running_delta = 0
            for option in self.options:
                option_number = option.number
                option_value = option.value
                option_delta = option_number - running_delta
                option_length = option.length()

                if option_delta < 13:
                    fmt += 'B'
                    delta = option_delta
                    ext_delta = 0
                elif 12 < option_delta < 269:
                    fmt += 'BB'
                    delta = 13
                    ext_delta = option_delta - 13
                elif 268 < option_delta:
                    fmt += 'BB'
                    delta = 14
                    ext_delta = option_delta - 269
                else:
                    raise SmpMessageFormatError('option number too high')
                running_delta += option_number

                if option_length < 13:
                    length = option_length
                    ext_length = 0
                elif 12 < option_length < 269:
                    fmt += 'B'
                    length = 13
                    ext_length = option_length - 13
                elif 268 < option_length:
                    fmt += 'B'
                    length = 14
                    ext_length = option_length - 269
                else:
                    raise SmpMessageFormatError('option length too long')

                values.append((delta << 4) | length)

                if ext_delta:
                    values.append(ext_delta)
                if ext_length:
                    values.append(ext_length)
                if option_value and option_length:
                    if option.type() == SMP_OPTION_TYPE_OPAQUE:
                        fmt += '{0}B'.format(option_length)
                        values.append(option_value)
                    elif option.type() == SMP_OPTION_TYPE_UINT:
                        fmt += '{0}B'.format(option_length)
                        values.append(option_value)
                    elif option.type() == SMP_OPTION_TYPE_STRING:
                        fmt += '{0}s'.format(option_length)
                        values.append(bytes(str(option_value), 'utf-8'))
                    else:
                        pass

        if self.payload:
            fmt += 'B'
            values.append(SMP_PAYLOAD_MARKER)
            if content_format == SMP_CONTENTFORMAT_TEXT_PLAIN:
                data = str(self.payload).encode('utf-8')
            elif content_format == SMP_CONTENTFORMAT_APPLICATION_EXI:
                raise SmpContentFormatError('content format exi is not supported')
            elif content_format == SMP_CONTENTFORMAT_APPLICATION_XML:
                data = str(self.payload).encode('utf-8')
            elif content_format == SMP_CONTENTFORMAT_APPLICATION_JSON:
                data = json.dumps(self.payload)
            elif content_format == SMP_CONTENTFORMAT_APPLICATION_LINKFORMAT:
                data = str(self.payload).encode('utf-8')
            elif content_format == SMP_CONTENTFORMAT_APPLICATION_OCTET_STREAM:
                data = self.payload
            else:
                raise SmpContentFormatError('content format {} is unknown'.format(content_format))
            fmt += '{0}s'.format(len(data))
            values.append(data)

        return struct.pack(fmt, *values)

    def __init__(self):
        self.ver = 1
        self.type = None
        self.tkl = 0
        self.code = None
        self.msgid = None
        self.addr = None
        self.random = None
        self.token = None
        self.options = []
        self.payload = None

    def add_option(self, option_number, option_value):
        self.options.append(SmpOption(option_number, option_value))
        self.options.sort()

    def content_format(self, cf):
        if self.payload:
            self.add_option(SMP_OPTION_CONTENT_FORMAT, cf)



#CoAP Client
class SmpClient(object):
    """docstring for SmpClient"""
    def __init__(self, ip, port=5683):
        self.ip = ip
        self.port = port
        self.addr = (self.ip, self.port)
        self.udp_send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.udp_recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_send_sock.bind(('192.168.3.104', self.port+1))
        #self.udp_send_sock.listen()

    def sendRequest(self):
        payload = SmpPayload('0', 0)
        smp_req = self.make_response(b'1234', 1, payload)
        smp_req.add_option(SMP_OPTION_URI_PATH,'v1')
        smp_req.add_option(SMP_OPTION_URI_PATH,'random')
        smp_msg = smp_req.serialize()
        smp_resp = self.send_msg(smp_msg, self.addr)

        smp_req = self.make_response(smp_resp.token, 1, payload)
        smp_req.random = smp_resp.random
        smp_req.add_option(SMP_OPTION_URI_PATH, 'v1')
        smp_req.add_option(SMP_OPTION_URI_PATH, 'test')
        smp_msg = SmpMessage.serialize(smp_req)
        smp_resp = self.send_msg(smp_msg, self.addr)


    def make_response(self, token, code, payload):
        response = SmpMessage()

        response.type = SMP_TYPE_NON_CONFIRMABLE
        response.code = code
        response.msgid = 1
        response.token = token
        response.addr = b'\xff\xff\xff\xff'
        response.random = b'\x00\x00\x00\x00'

        response.content_format(payload.content_format)

        return response

    def send_msg(self, datagram, destination):
        #datagram = smp_msg.to_bytes()
        self.udp_send_sock.sendto(datagram, destination)
        datagram, addr = self.udp_send_sock.recvfrom(1152)
        smp_req = SmpMessage.deserialize(datagram)

        return smp_req
        #print(self.udp_send_sock.recv(1024))