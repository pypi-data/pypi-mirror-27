import os
import pytest
import json
from shapely.geometry import shape
from geomark.geomark import Geomark
from geomark.config import LOGGER as logger
from . import data as _data


def strip_variable_properties(data, method='feature'):
    """ When a Geomark object is created by Geomark BC, it comes with some variable data such as a unique ID and URL,
    as well as the CreateDate and Expiry date.  We don't need to compare these.

    Presumably the Geomark folks won't change the properties they pass back without alerting their subscribers or
    making such a change a part of a new release, as such there should be ample warning.  If this becomes a problem
    in the future we can discuss simply stripping the properties objects since we mostly care about accurate geometries.

    :param data: The data returned by the given Geomark method
    :param method: The method used to obtain data
    :return: a copy of the data object with variable properties removed
    """
    if method != 'info':
        del data['properties']['id']
        del data['properties']['url']

        try:
            del data['properties']['createDate']
            del data['properties']['expiryDate']
        except KeyError:
            pass
    else:
        del data['id']
        del data['url']
        del data['createDate']
        del data['expiryDate']
        del data['googleMapsUrl']
        del data['googleEarthUrl']
        del data['resourceLinks']

    return data


def get_expected_value(geom_type, method):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name_template = os.path.join(dir_path, 'files/expected/{}_{}.json')

    with open(file_name_template.format(geom_type, method), 'r') as f:
        file_contents = f.read()

    return json.loads(file_contents)


def test_create(geo_file):
    # Perhaps the use of the Geomark.feature() method makes this sort of double as a test_feature test...
    expected = get_expected_value(geo_file['geom_type'], 'feature')  # variable properties have already been removed.
    gm = Geomark.create(format=geo_file['format'], body=geo_file['data'])
    geojson = strip_variable_properties(json.loads(gm.feature('geojson').decode('utf8')))

    assert expected == geojson


@pytest.mark.dependency(depends=_data.depends_create)
def test_bbox(geomark_object):
    expected = get_expected_value(geomark_object['geom_type'], 'boundingBox')
    bbox = strip_variable_properties(json.loads(geomark_object['gm'].boundingBox('geojson').decode('utf8')),
                                     'boundingBox')
    assert expected == bbox


@pytest.mark.dependency(depends=_data.depends_create)
def test_feature(geomark_object):
    # variable properties have already been removed.
    expected = get_expected_value(geomark_object['geom_type'], 'feature')
    feature = strip_variable_properties(json.loads(geomark_object['gm'].feature('geojson').decode('utf8')))
    assert expected == feature


@pytest.mark.dependency(depends=_data.depends_create)
def test_info(geomark_object):
    expected = get_expected_value(geomark_object['geom_type'], 'info')
    info = strip_variable_properties(json.loads(geomark_object['gm'].info().decode('utf8')), 'info')
    assert expected == info


@pytest.mark.dependency(depends=_data.depends_create)
def test_parts(geomark_object):
    expected = get_expected_value(geomark_object['geom_type'], 'parts')
    parts = strip_variable_properties(json.loads(geomark_object['gm'].parts('geojson').decode('utf8')), 'parts')
    assert expected == parts


@pytest.mark.dependency(depends=_data.depends_create)
def test_point(geomark_object):
    expected = get_expected_value(geomark_object['geom_type'], 'point')
    point = strip_variable_properties(json.loads(geomark_object['gm'].point('geojson').decode('utf8')), 'point')
    assert expected == point


@pytest.mark.dependency(depends=_data.depends_create)
def test_copy(geomark_object):
    expected = get_expected_value(geomark_object['geom_type'], 'copy_200')
    gm = geomark_object['gm'].copy(bufferMetres=200)
    copy = strip_variable_properties(json.loads(gm.feature('geojson').decode('utf8')), 'feature')
    assert expected == copy


@pytest.mark.dependency(depends=_data.depends_create)
def test_copy_multiple(geomark_ids):
    expected = shape(get_expected_value('copy', 'multiple')['geometry'])

    gm = Geomark(geomarkId=geomark_ids['point'])
    gm2 = gm.copy(geomarkUrl=[geomark_ids['point'], geomark_ids['linestring'], geomark_ids['polygon']], allowOverlap=True, bufferMetres=0.1)
    copy_multiple = shape(json.loads(gm2.feature('geojson').decode('utf8'))['geometry'])

    # overlapping multi polygon should be invalid
    assert not copy_multiple.is_valid

    # put the geometry components in order by area
    sort_expected_geom = sorted(expected.geoms, key=lambda geom: geom.area)
    sort_copy_geoms = sorted(copy_multiple.geoms, key=lambda geom: geom.area)

    # test geometry components for equality and validity
    for i in range(0, len(sort_copy_geoms)):
        assert sort_copy_geoms[i].is_valid
        assert sort_expected_geom[i].equals(sort_copy_geoms[i])
