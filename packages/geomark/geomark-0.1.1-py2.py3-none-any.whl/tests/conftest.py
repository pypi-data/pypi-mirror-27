import os
import pytest

from geomark import config, Geomark
from . import data


@pytest.fixture(scope='function', params=data.dependency_geo_files)
def geo_file(request):
    filename = request.module.__file__
    with open(os.path.join(os.path.dirname(filename), "files/{}".format(request.param['file'])), 'r') as f:
        yield {
            'format': request.param['format'],
            'data': f.read(),
            'geom_type': request.param['geom_type']
        }


@pytest.fixture(scope='module', params=data.geo_files)
def geomark_object(request):
    filename = request.module.__file__
    with open(os.path.join(os.path.dirname(filename), "files/{}".format(request.param['file'])), 'r') as f:
        yield {
            'gm': Geomark.create(format=request.param['format'], body=f.read()),
            'geom_type': request.param['geom_type']
        }


@pytest.fixture(scope='function')
def geomark_ids(request):
    fixture = dict()
    geo_files = [x.args[0] for x in filter(lambda y: y.args[0]['format'] == 'kml', data.geo_files)]

    for file in geo_files:
        with open(os.path.join(os.path.dirname(request.module.__file__), "files/{}".format(file['file'])), 'r') as f:
            gm = Geomark.create(format=file['format'], body=f.read())
            fixture[file['geom_type']] = gm.geomarkId

    return fixture
