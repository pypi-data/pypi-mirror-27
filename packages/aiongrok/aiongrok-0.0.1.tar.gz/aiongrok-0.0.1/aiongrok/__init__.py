import logging

import aiohttp

version = '0.0.1'

logging.getLogger(__name__).addHandler(logging.NullHandler())


class TunnelError(Exception):
    """Exception which represents tunnel errors."""
    pass


class TunnelNotFound(TunnelError):
    """Exception which would be used in case tunnel cannot be found."""
    pass


class Tunnel:
    def __init__(self, *, proto, public_url, uri, name):
        self.name = name
        self.uri = uri
        self.proto = proto
        self.public_url = public_url

    def __str__(self):
        return '{}, {}'.format(self.name, self.public_url)


class TunnelsCollection(list):
    def get_any_http_tunnel(self):
        return self.__get_any_tunnel('http')

    def get_any_https_tunnel(self):
        return self.__get_any_tunnel('https')

    def __get_any_tunnel(self, proto):
        for tunnel in self:
            if tunnel.proto == proto:
                logging.debug('tunnel with proto {} found'.format(proto))
                return tunnel
        message = 'any {} tunnel not found'.format(proto)
        logging.warning(message)
        raise TunnelNotFound(message)


class Session:
    api_url = 'http://127.0.0.1:4040/api/'

    def __init__(self, *, api_url=None):
        if api_url is not None:
            self.api_url = api_url
        self.session = aiohttp.ClientSession()

    def close(self):
        self.session.close()

    async def get_tunnels(self):
        url = '{}tunnels'.format(self.api_url)
        async with self.session.get(url) as response:
            data = await response.json()
            if response.status != 200:
                logging.warning(data['msg'])
                raise TunnelNotFound(data['msg'])
        tunnels = TunnelsCollection()
        for item in data['tunnels']:
            tunnels.append(self.__make_tunnel(item))
        return tunnels

    async def get_tunnel(self, name):
        url = '{}tunnels/{}'.format(self.api_url, name)
        async with self.session.get(url) as response:
            data = await response.json()
            if response.status != 200:
                logging.warning(data['msg'])
                raise TunnelNotFound(data['msg'])
        return self.__make_tunnel(data)

    @staticmethod
    def __make_tunnel(item):
        return Tunnel(name=item['name'],
                      uri=item['uri'],
                      proto=item['proto'],
                      public_url=item['public_url'])
