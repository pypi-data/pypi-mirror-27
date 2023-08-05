import asyncio
import ssl
import warnings

from pypeman import endpoints, channels, nodes, message

import aiohttp
from aiohttp import web

class HTTPEndpoint(endpoints.BaseEndpoint):
    """
    Endpoint to receive HTTP connection from outside.

    :param http_args: dict to pass as **kwargs** to aiohttp.Application for example for
        `client_max_size`
    """

    def __init__(self, adress=None, address='127.0.0.1', port='8080', loop=None, http_args=None):
        super().__init__()
        self.http_args = http_args or {}
        self.ssl_context = self.http_args.pop('ssl_context', None)

        if adress is not None:
            warnings.warn("HTTPEndpoint 'adress' param is deprecated. Replace it by 'address'", DeprecationWarning)
            address = adress

        self._app = None
        self.address = address
        self.port = port
        self.loop = loop or asyncio.get_event_loop()

    def add_route(self, *args, **kwargs):
        if self._app is None:
            self._app = web.Application(**self.http_args)

        self._app.router.add_route(*args, **kwargs)

    async def start(self):
        if self._app is not None:
            srv = await self.loop.create_server(
                protocol_factory=self._app.make_handler(),
                host=self.address,
                port=self.port,
                ssl=self.ssl_context
            )
            print("Server started at http{}://{}:{}".format(
                's' if self.ssl_context else '',
                self.address,
                self.port
            ))
            return srv
        else:
            print("No HTTP route.")

class HttpChannel(channels.BaseChannel):
    """
    Channel that handles Http connection. The Http message is the message payload and some headers
    become metadata of message. Needs ``aiohttp`` python dependency to work.

    :param endpoint: HTTP endpoint used to get connections.
    :param method: Method filter.
    :param url: Only matching urls messages will be sent to this channel.
    :param encoding: Encoding of message. Default to 'utf-8'.

    """
    app = None

    def __init__(self, *args, endpoint=None, method='*', url='/', encoding=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.method = method
        self.url = url
        self.encoding = encoding
        if endpoint is None:
            raise TypeError('Missing "endpoint" argument')
        self.http_endpoint = endpoint

    async def start(self):
        await super().start()
        if self._first_start:
            self.http_endpoint.add_route(self.method, self.url, self.handle_request)

    async def handle_request(self, request):
        content = await request.text()
        msg = message.Message(content_type='http_request', payload=content, meta={'method': request.method})
        try:
            result = await self.handle(msg)
            encoding = self.encoding or 'utf-8'
            return web.Response(body=result.payload.encode(encoding), status=result.meta.get('status', 200))

        except channels.Dropped:
            return web.Response(body="Dropped".encode('utf-8'), status=200)
        except Exception as e:
            return web.Response(body=str(e).encode('utf-8'), status=503)


class HttpRequest(nodes.BaseNode):
    """
        Http request node
        :param url: url to send.
        :param method: 'get', 'put' or 'post', use meta['method'] if None, Default to 'get'.
        :param headers: headers for request, use meta['headers'] if None.
        :param auth: tuple or aiohttp.BasicAuth object.
        :param verify: verify ssl. Default True.
        :param params: get params in dict. List for multiple elements, ex : {'param1': 'omega', param2: ['alpha', 'beta']}
        :param client_cert: tuple with .crt and .key path
    """

    def __init__(self, url, *args, method=None, headers=None, auth=None, verify=True, params=None, client_cert=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url
        self.method = method
        self.headers = headers
        self.auth = auth
        self.verify = verify
        self.params = params
        self.client_cert = client_cert
        self.url = self.url.replace('%(meta.', '%(')
        self.payload_in_url_dict = 'payload.' in self.url
        # TODO: create used payload keys for better perf of generate_request_url()

    def generate_request_url(self, msg):
        url_dict = msg.meta
        if self.payload_in_url_dict:
            url_dict = dict(url_dict)
            try:
                for key, val in msg.payload.items():
                    url_dict['payload.' + key] = val
            except AttributeError:
                self.channel.logger.exception("Payload must be a python dict if used to generate url. This can be fixed using JsonToPython node before your RequestNode")
                raise
        return self.url % url_dict

    async def handle_request(self, msg):
        """ generate url and handle request """
        url = self.generate_request_url(msg)
        loop = self.channel.loop
        conn = None
        ssl_context = None
        if self.client_cert:
            if self.verify:
                ssl_context = ssl.create_default_context()
            else:
                ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            ssl_context.load_cert_chain(self.client_cert[0], self.client_cert[1])
            conn = aiohttp.TCPConnector(ssl_context=ssl_context, loop=loop)
        else:
            conn = aiohttp.TCPConnector(verify_ssl=self.verify, loop=loop)

        headers = nodes.choose_first_not_none(self.headers, msg.meta.get('headers'))
        method = nodes.choose_first_not_none(self.method, msg.meta.get('method'), 'get')
        params = nodes.choose_first_not_none(self.params, msg.meta.get('params'))

        get_params = None
        if params:
            get_params = []
            for key, param in params.items():
                if isinstance(param, list):
                    for value in param:
                        get_params.append((key, value))
                else:
                    get_params.append((key, param))

        if isinstance(self.auth, tuple):
            basic_auth = aiohttp.BasicAuth(self.auth[0], self.auth[1])
        else:
            basic_auth = self.auth

        data = None
        if method in ['put', 'post']:
            data = msg.payload
        with aiohttp.ClientSession(connector=conn) as session:
            resp = await session.request(
                    method=method,
                    url=url,
                    auth=basic_auth,
                    headers=headers,
                    params=get_params,
                    data=data
                    )
            resp_text =  await resp.text()
            return str(resp_text)

    async def process(self, msg):
        """ handles request """
        msg.payload = await self.handle_request(msg)
        return msg


class RequestNode(HttpRequest):
    def __init__(self, *args, **kwargs):
        warnings.warn("RequestNode node is deprecated. New name is 'HttpRequest' node", DeprecationWarning)
        super().__init__(*args, **kwargs)
