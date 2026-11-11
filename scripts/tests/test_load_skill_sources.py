"""Offline tests of how load_skill_sources.py reads SKILL.md.

Run: python3 -I scripts/tests/test_load_skill_sources.py
"""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "qgis"))
import load_skill_sources as loader  # noqa: E402

SKILL = os.path.join(HERE, "..", "..", "skills", "byg-gis-app", "SKILL.md")


class ProbesFromRealSkill(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.probes = loader.probes_from_skill(loader.read_skill(SKILL))
        cls.by_name = {p.name: p for p in cls.probes}

    def test_example_urls_are_requested_as_written(self):
        probe = self.by_name["dai:fredede_omr (eksempel)"]
        self.assertTrue(probe.example)
        self.assertIn("bbox=9.7,56.9,10.2,57.2,CRS:84", probe.url)

    def test_named_wfs_layers_get_a_sample_request(self):
        probe = self.by_name["dai:ramsar_omr"]
        self.assertFalse(probe.example)
        self.assertIn("miljoeportal.dk/geoserver/ows?", probe.url)
        self.assertIn("count=%d" % loader.SAMPLE_COUNT, probe.url)

    def test_tema_placeholder_takes_the_layer_prefix(self):
        self.assertIn("wfs2-miljoegis.mim.dk/stoej/ows?", self.by_name["stoej:b2_dk_aggroad_lden"].url)

    def test_layers_with_an_example_are_not_sampled_again(self):
        names = [p.name for p in self.probes]
        self.assertNotIn("dai:fredede_omr", names)
        self.assertNotIn("natur:natura_2000_omraader", names)

    def test_lon_lat_placeholder_gets_the_test_point(self):
        probe = self.by_name["stoej:b4_dk_aggroad_lnight (eksempel)"]
        self.assertNotIn("LON", probe.url)
        self.assertIn("POINT(9.92%2057.05)", probe.url)

    def test_dmi_collections_expand_the_dots(self):
        url = self.by_name["metObs/collections/station/items"].url
        self.assertEqual(url, "https://opendataapi.dmi.dk/v2/metObs/collections/station/items?limit=50")

    def test_special_kinds(self):
        kinds = {p.kind for p in self.probes}
        self.assertEqual(kinds, {"geojson", "csv", "overpass", "style"})
        overpass = next(p for p in self.probes if p.kind == "overpass")
        self.assertTrue(overpass.body.startswith("data=%5Bout%3Ajson%5D"))

    def test_every_source_section_is_covered(self):
        sections = {p.section for p in self.probes}
        for section in ["OpenFreeMap", "Danmarks Miljøportal", "MiljøGIS", "Støjkortlægning af vejstøj",
                        "DMI Open Data", "Danmarks Statistik, Statbank", "Kommunegrænser", "Vejdirektoratet",
                        "Københavns Kommune", "Overpass API"]:
            self.assertIn(section, sections)


class OverpassToGeojson(unittest.TestCase):
    def test_nodes_and_centres_become_points(self):
        data = {"elements": [
            {"type": "node", "id": 1, "lat": 57.0, "lon": 9.9, "tags": {"name": "A"}},
            {"type": "way", "id": 2, "center": {"lat": 57.1, "lon": 9.8}},
        ]}
        features = loader.overpass_to_geojson(data)["features"]
        self.assertEqual(features[0]["geometry"]["coordinates"], [9.9, 57.0])
        self.assertEqual(features[1]["geometry"]["coordinates"], [9.8, 57.1])
        self.assertEqual(features[1]["properties"]["osm_type"], "way")


if __name__ == "__main__":
    unittest.main()
