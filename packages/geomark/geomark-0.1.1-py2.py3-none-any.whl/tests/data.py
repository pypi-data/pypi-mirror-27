import pytest


depends_create = [
    "create_point_kml",
    "create_line_kml",
    "create_polygon_kml",
    "create_point_geojson",
    "create_line_geojson",
    "create_polygon_geojson"
]

dependency_geo_files = [
    pytest.mark.dependency(name="create_point_kml")({'format': 'kml', 'file': 'point.kml', 'geom_type': 'point'}),
    pytest.mark.dependency(name="create_line_kml")({'format': 'kml', 'file': 'line.kml', 'geom_type': 'linestring'}),
    pytest.mark.dependency(name="create_polygon_kml")({'format': 'kml', 'file': 'polygon.kml', 'geom_type': 'polygon'}),
    pytest.mark.dependency(name="create_point_geojson")({'format': 'geojson', 'file': 'point.geojson', 'geom_type': 'point'}),
    pytest.mark.dependency(name="create_line_geojson")({'format': 'geojson', 'file': 'line.geojson', 'geom_type': 'linestring'}),
    pytest.mark.dependency(name="create_polygon_geojson")({'format': 'geojson', 'file': 'polygon.geojson', 'geom_type': 'polygon'})
]

geo_files = [
    pytest.mark.dependency(depends=depends_create)({'format': 'kml', 'file': 'point.kml', 'geom_type': 'point'}),
    pytest.mark.dependency(depends=depends_create)({'format': 'kml', 'file': 'line.kml', 'geom_type': 'linestring'}),
    pytest.mark.dependency(depends=depends_create)({'format': 'kml', 'file': 'polygon.kml', 'geom_type': 'polygon'}),
    pytest.mark.dependency(depends=depends_create)({'format': 'geojson', 'file': 'point.geojson', 'geom_type': 'point'}),
    pytest.mark.dependency(depends=depends_create)({'format': 'geojson', 'file': 'line.geojson', 'geom_type': 'linestring'}),
    pytest.mark.dependency(depends=depends_create)({'format': 'geojson', 'file': 'polygon.geojson', 'geom_type': 'polygon'})
]
