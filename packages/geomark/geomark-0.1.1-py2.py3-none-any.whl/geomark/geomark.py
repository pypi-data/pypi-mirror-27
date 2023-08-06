import os
import requests
# from six.moves.urllib.parse import urlparse

from . import config as _config

_base_url = "{protocol}://apps.gov.bc.ca/pub/geomark"
_gm_id_base = _base_url + '/geomarks/{geomarkId}'


class Geomark:

    def __init__(self, geomarkId=None, geomarkUrl=None, config=_config):
        self.config = config

        self.logger = self.config.LOGGER

        if not geomarkId and not geomarkUrl:
            raise SyntaxError("One of geomarkId or geomarkUrl are required kwargs")

        if geomarkId:
            self.geomarkUrl = self.config.GEOMARK_ID_BASE_URL.format(
                protocol=config.PROTOCOL,
                geomarkId=geomarkId,
            )
            self.geomarkId = geomarkId
        else:
            self.geomarkId, self.geomarkUrl, self.config.PROTOCOL = self._parse_geomark_url(geomarkUrl)

        self.logger.info('Initiated Geomark object with the following parameters: '
                         'geomarkId={geomarkId}; '
                         'geomarkUrl={geomarkUrl}; '
                         'protocol={protocol}; '
                         'custom_config: {custom_config}'.format(

            geomarkId=geomarkId,
            geomarkUrl=geomarkUrl,
            protocol=config.PROTOCOL,
            custom_config='YES' if config is _config else 'NO')
        )

    def _parse_geomark_url(self, url):
        """
        Parse the geomarkUrl for GeomarkId, protocol, and strip off the format specifier if one is present
        :param url:
        :return: GeomarkId, GeomarkUrl (no format), PROTOCOL
        """
        parsed = requests.compat.urlparse(url)
        tail = parsed.path.split('/')[-1]
        gmid, format = os.path.splitext(tail)
        if format:
            url = url.replace(format, '')

        return gmid, url, parsed.scheme

    def boundingBox(self, fileFormatExtension='json', srid=None):
        url = self.geomarkUrl + '/boundingBox.{fileFormatExtension}'.format(
            fileFormatExtension=fileFormatExtension,
        )
        return self._handle_get(requests.get(url, params={'srid': srid} if srid else None))

    def feature(self, fileFormatExtension='json', srid=None):
        url = self.geomarkUrl + '/feature.{fileFormatExtension}'.format(
            fileFormatExtension=fileFormatExtension,
        )
        return self._handle_get(requests.get(url, params={'srid': srid} if srid else None))

    def info(self, fileFormatExtension='json', srid=None):
        url = self.geomarkUrl + '.{fileFormatExtension}?'.format(
            fileFormatExtension=fileFormatExtension,
        )
        return self._handle_get(requests.get(url, params={'srid': srid} if srid else None))

    def parts(self, fileFormatExtension='json', srid=None):
        url = self.geomarkUrl + '/parts.{fileFormatExtension}'.format(
            fileFormatExtension=fileFormatExtension,
        )
        return self._handle_get(requests.get(url, params={'srid': srid} if srid else None))

    def point(self, fileFormatExtension='json', srid=None):
        url = self.geomarkUrl + '/point.{fileFormatExtension}'.format(
            fileFormatExtension=fileFormatExtension,
        )
        return self._handle_get(requests.get(url, params={'srid': srid} if srid else None))

    def copy(self,
             geomarkUrl=None,
             resultFormat='json',
             allowOverlap=False,
             # callback              ---- Not supported
             # redirectUrl           ---- Not supported
             # failureRedirectUrl    ---- Not supported
             bufferMetres=None,
             bufferJoin=None,
             bufferCap=None,
             bufferMitreLimit=None,
             bufferSegments=None):
        """
        TIP: If you do a straight copy without altering any of the parameters the geomark
        server will notice that the geometry is identical and instead of giving you back a new Geomark
        instance you will simply be given back the original. An alternative would be to specify a tiny buffer
        on the geometry using the bufferMeters kwarg.
        :param geomarkUrl: can be geomarkId or the complete geomarkUrl. Can be a python list of strings or a single string.
        :param resultFormat:
        :param allowOverlap:
        :param bufferMetres:
        :param bufferJoin:
        :param bufferCap:
        :param bufferMitreLimit:
        :param bufferSegments:
        :return:
        """

        # collect the method's named args -- there has got to be a better way. Going the inspect route causes problems with 2.7.
        query = {
            'geomarkUrl': geomarkUrl,
            'resultFormat': resultFormat,
            'allowOverlap': allowOverlap,
            'bufferMetres': bufferMetres,
            'bufferJoin': bufferJoin,
            'bufferCap': bufferCap,
            'bufferMitreLimit': bufferMitreLimit,
            'bufferSegments': bufferSegments
        }

        url = self.config.GEOMARK_BASE_URL.format(protocol=self.config.PROTOCOL) + '/geomarks/copy'

        # use the instance geomarkUrl if the kwarg isn't present:
        if not geomarkUrl:
            query.update({'geomarkUrl': self.geomarkUrl})

        del query['allowOverlap']  # allowOverlap should not go in the query.
        form_data = {'allowOverlap': allowOverlap}

        params = self._validate_post_kwargs(**query)
        r = requests.post(url, data=form_data, params=params)
        return Geomark._handle_post(r, config=self.config)

    @staticmethod
    def create(
            format=None,
            srid=4326,
            resultFormat='json',
            multiple=False,
            allowOverlap=False,
            # callback              ---- Not supported
            # redirectUrl           ---- Not supported
            # failureRedirectUrl    ---- Not supported
            bufferMetres=None,
            bufferJoin=None,
            bufferCap=None,
            bufferMitreLimit=None,
            bufferSegments=None,
            body=None,
            extra_kwargs={}):
        """
        Create a Geomark layer
        :param format:
        :param srid:
        :param resultFormat:
        :param multiple:
        :param allowOverlap:
        :param bufferMetres:
        :param bufferJoin:
        :param bufferCap:
        :param bufferMitreLimit:
        :param bufferSegments:
        :param body:
        :param extra_kwargs: put the overridden config object here, key: "config"
        :return:
        """
        # collect the method's named args -- there has got to be a better way. Going the inspect route causes problems with 2.7.
        kwargs = {
            'format': format,
            'srid': srid,
            'resultFormat': resultFormat,
            'multiple': multiple,
            'allowOverlap': allowOverlap,
            'bufferMetres': bufferMetres,
            'bufferJoin': bufferJoin,
            'bufferCap': bufferCap,
            'bufferMitreLimit': bufferMitreLimit,
            'bufferSegments': bufferSegments,
            'body': body
        }
        form_data = Geomark._validate_post_kwargs(**kwargs)

        config = extra_kwargs.get("config", _config)
        url = config.GEOMARK_BASE_URL.format(protocol=config.PROTOCOL) + '/geomarks/new'

        return Geomark._handle_post(requests.post(url, data=form_data), config=config)

    @staticmethod
    def _handle_get(response, **kwargs):
        config = kwargs.get("config", _config)
        if response.ok:
            return response.content
        else:
            config.LOGGER.error("Server responded with: " + response.text)
            response.raise_for_status()

    @staticmethod
    def _handle_post(response, **kwargs):
        config = kwargs.get("config", _config)
        if response.ok:
            url = response.url
            response.close()
            return Geomark(geomarkUrl=url)
        else:
            config.LOGGER.error("Server responded with: " + response.text)
            response.raise_for_status()

    @staticmethod
    def _validate_post_kwargs(**kwargs):
        """
        Used by both create() and copy()
        Doesn't do anything right now.
        We don't need to pull out Nones because requests will do that for us.
        :param kwargs:
        :return:
        """
        # TODO Actually validate post kwargs.
        return kwargs
