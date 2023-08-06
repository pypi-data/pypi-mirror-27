import logging

# TODO set LOG_LEVEL to info when we don't actively need debugging anymore.
LOG_LEVEL = logging.DEBUG  # Options include... CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET

LOGGER = logging.getLogger('geomark')
LOGGER.setLevel(LOG_LEVEL)

# The default StreamHandler writes to stderr
_ch = logging.StreamHandler()

# Create a simple formatter...
_formatter = logging.Formatter('%(name)s:%(levelname)s (%(asctime)s) - %(message)s')
_ch.setFormatter(_formatter)

LOGGER.addHandler(_ch)

# These will probably never change
# If, for some reason they ever do, note the names of the keywords, as they are specifically referred to by name.
PROTOCOL = 'https'
GEOMARK_BASE_URL = '{protocol}://apps.gov.bc.ca/pub/geomark'
GEOMARK_ID_BASE_URL = GEOMARK_BASE_URL + '/geomarks/{geomarkId}'
GEOMARK_GROUP_BASE_URL = GEOMARK_BASE_URL + '/geomarkGroups/{geomarkGroupId}'
