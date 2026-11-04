"""Loads every Data source the Build skill names into QGIS, for a manual check.

In a chat the agent writes the App from the SKILL.md text alone, so every URL,
layer name and field name there has to be right as written. This script reads
the "Datakilder" part of skills/byg-gis-app/SKILL.md and requests:

- every example URL, exactly as written (LON/LAT placeholders get TEST_POINT),
- a sample of every layer or collection the skill only names,
- the Overpass example query and the OpenFreeMap style.

In QGIS: open the Python console, open this file in its editor and press Run.
Each answer becomes a layer, grouped by skill section, and Statbank is joined
onto Kommunegrænser. A report is printed to the console.

Without QGIS: python3 -I scripts/qgis/load_skill_sources.py [SKILL.md] prints
the same report as Markdown.
"""

import csv
import io
import json
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field

# Path or URL of the SKILL.md to check. None means the copy in this repo, or
# the one on GitHub if this file's location is unknown (the QGIS console).
SKILL_MD = None
SKILL_MD_ON_GITHUB = ("https://raw.githubusercontent.com/steenhulthin/"
                      "byg-din-egen-gis-applikation/trunk/skills/byg-gis-app/SKILL.md")
TEST_POINT = (9.92, 57.05)  # lon, lat in Aalborg, for the LON%20LAT placeholder
SAMPLE_COUNT = 50  # features requested for layers the skill names without a URL
TIMEOUT = 90
ORIGIN = "https://example.github.io"
USER_AGENT = ("byg-din-egen-gis-applikation QGIS check "
              "(+https://github.com/steenhulthin/byg-din-egen-gis-applikation)")
GROUP_NAME = "Byg-gis-app datakilder"
KOMMUNER_FILE = "kommuneinddeling.geojson"


@dataclass
class Probe:
    section: str
    name: str
    url: str
    kind: str  # geojson, csv, overpass or style
    example: bool  # True if the URL is written out in the skill
    body: str = ""


@dataclass
class Result:
    probe: Probe
    status: int = 0
    cors: str = ""
    size: int = 0
    seconds: float = 0.0
    notes: list = field(default_factory=list)
    count: int | None = None
    null_geometries: int = 0
    fields: list = field(default_factory=list)
    text: str = ""  # decoded body, UTF-8 GeoJSON for overpass


def read_skill(location):
    if re.match(r"https?://", location):
        with urllib.request.urlopen(location, timeout=TIMEOUT) as answer:
            return answer.read().decode("utf-8")
    with open(location, encoding="utf-8") as file:
        return file.read()


def default_skill_location():
    if SKILL_MD:
        return SKILL_MD
    try:
        here = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        return SKILL_MD_ON_GITHUB
    local = os.path.join(here, "..", "..", "skills", "byg-gis-app", "SKILL.md")
    return local if os.path.exists(local) else SKILL_MD_ON_GITHUB


def sections(skill):
    """Yields (heading, text) for the "Datakilder" part, split at ### headings."""
    part = skill.split("\n## Datakilder", 1)[1].split("\n## ", 1)[0]
    chunks = re.split(r"\n### ", part)
    yield "Fælles for WFS", chunks[0]
    for chunk in chunks[1:]:
        heading, _, text = chunk.partition("\n")
        yield heading.split(" (")[0].strip(), text


def kind_of(url):
    if "/styles/" in url:
        return "style"
    if "/CSV?" in url:
        return "csv"
    if "request=GetFeature" in url or "/items?" in url or url.endswith(".geojson"):
        return "geojson"
    return None


def wfs_sample_url(base, layer):
    prefix = layer.split(":")[0]
    return (base.replace("{tema}", prefix) +
            "?service=WFS&version=2.0.0&request=GetFeature&typeNames=" + layer +
            "&outputFormat=application/json&srsName=EPSG:4326&count=%d" % SAMPLE_COUNT)


def probes_from_skill(skill):
    probes = []
    lon, lat = TEST_POINT
    for section, text in sections(skill):
        ticked = re.findall(r"`([^`\n]+)`", text)
        address = re.search(r"Adresse: `([^`]+)`", text)
        base = address.group(1) if address else ""
        covered = set()
        for token in ticked:
            kind = kind_of(token) if token.startswith("http") else None
            if not kind:
                continue
            url = token.replace("LON%20LAT", "%s%%20%s" % (lon, lat))
            name = re.search(r"typeNames=([^&]+)", url)
            name = name.group(1) if name else "/".join(url.split("?")[0].split("/")[-2:])
            covered.add(name)
            covered.add(urllib.parse.urlsplit(url).path)
            probes.append(Probe(section, name + " (eksempel)", url, kind, True))
        if base.endswith("/ows"):
            for token in ticked:
                if re.fullmatch(r"[a-z0-9_]+:[A-Za-z0-9_]+", token) and token not in covered:
                    covered.add(token)
                    probes.append(Probe(section, token, wfs_sample_url(base, token), "geojson", False))
        if base.endswith("/..."):
            root = base[:-4]
            for token in ticked:
                path = urllib.parse.urlsplit(root + token[3:]).path
                if token.startswith(".../") and token.endswith("/items") and path not in covered:
                    covered.add(path)
                    probes.append(Probe(section, token[4:], "%s%s?limit=%d" % (root, token[3:], SAMPLE_COUNT),
                                        "geojson", False))
        for token in ticked:
            if token.startswith("[out:json]") and base:
                probes.append(Probe(section, "Overpass-forespørgsel (eksempel)", base, "overpass", True,
                                    "data=" + urllib.parse.quote(token)))
    return probes


def request(url, body=""):
    headers = {"Origin": ORIGIN, "User-Agent": USER_AGENT}
    data = body.encode("ascii") if body else None
    started = time.monotonic()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data, headers), timeout=TIMEOUT) as answer:
            return answer.status, answer.headers, answer.read(), time.monotonic() - started
    except urllib.error.HTTPError as error:
        return error.code, error.headers, error.read(), time.monotonic() - started


def overpass_to_geojson(data):
    features = []
    for element in data.get("elements", []):
        point = element if "lat" in element else element.get("center")
        geometry = {"type": "Point", "coordinates": [point["lon"], point["lat"]]} if point else None
        properties = dict(element.get("tags", {}), osm_type=element.get("type"), osm_id=element.get("id"))
        features.append({"type": "Feature", "geometry": geometry, "properties": properties})
    return {"type": "FeatureCollection", "features": features}


def run(probe):
    result = Result(probe)
    try:
        result.status, headers, raw, result.seconds = request(probe.url, probe.body)
    except Exception as error:  # timeouts and DNS errors end up here
        result.notes.append("ingen svar: %s" % error)
        return result
    result.size = len(raw)
    result.cors = headers.get("Access-Control-Allow-Origin") or ""
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("iso-8859-1")
        result.notes.append("ikke UTF-8, læst som ISO-8859-1")
    if text.startswith("﻿"):
        text = text[1:]
        result.notes.append("starter med BOM")
    if result.status != 200:
        result.notes.append("svar: " + " ".join(text[:120].split()))
        return result
    try:
        if probe.kind in ("geojson", "overpass", "style"):
            data = json.loads(text)
            if probe.kind == "overpass":
                data = overpass_to_geojson(data)
                text = json.dumps(data, ensure_ascii=False)
            if probe.kind == "style":
                result.count = len(data.get("layers", []))
                result.fields = sorted(data.get("sources", {}))
            else:
                features = data["features"]
                result.count = len(features)
                result.null_geometries = sum(1 for f in features if not f.get("geometry"))
                result.fields = sorted({key for f in features for key in (f.get("properties") or {})})
        elif probe.kind == "csv":
            rows = list(csv.reader(io.StringIO(text), delimiter=";"))
            result.count = len(rows) - 1
            result.fields = rows[0]
    except (ValueError, KeyError, TypeError, IndexError) as error:
        result.notes.append("uventet format: %s: %s" % (type(error).__name__, " ".join(text[:120].split())))
    result.text = text
    return result


def report(results):
    lines = ["| Afsnit | Kilde | HTTP | CORS | Objekter | Uden geometri | KB | Sek. | Bemærkninger |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        lines.append("| %s | %s | %s | %s | %s | %s | %d | %.1f | %s |" % (
            r.probe.section, r.probe.name, r.status or "–", r.cors or "mangler",
            "–" if r.count is None else r.count, r.null_geometries or "", r.size // 1024, r.seconds,
            "; ".join(r.notes)))
    lines += ["", "Felter pr. kilde:", ""]
    for r in results:
        if r.fields:
            lines.append("- **%s / %s:** %s" % (r.probe.section, r.probe.name, ", ".join(r.fields)))
    return "\n".join(lines)


def load_into_qgis(results):
    from qgis.core import (QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject, QgsRectangle,
                           QgsVectorLayer, QgsVectorLayerJoinInfo, QgsVectorTileLayer)
    from qgis.utils import iface

    project = QgsProject.instance()
    root = project.layerTreeRoot()
    old = root.findGroup(GROUP_NAME)
    if old:
        root.removeChildNode(old)
    group = root.insertGroup(0, GROUP_NAME)
    folder = tempfile.mkdtemp(prefix="byg-gis-app-")
    kommuner, statbank = None, None

    for number, r in enumerate(results):
        if r.count is None:
            continue
        section = group.findGroup(r.probe.section) or group.addGroup(r.probe.section)
        if r.probe.kind == "style":
            style = json.loads(r.text)
            tilejson = next((s["url"] for s in style["sources"].values() if "url" in s), None)
            with urllib.request.urlopen(tilejson, timeout=TIMEOUT) as answer:
                tiles = json.load(answer)["tiles"][0]
            uri = "type=xyz&url=%s&zmax=14&styleUrl=%s" % (urllib.parse.quote(tiles, safe=":/{}"), r.probe.url)
            layer = QgsVectorTileLayer(uri, r.probe.name)
            if layer.isValid():
                layer.loadDefaultStyle()
                project.addMapLayer(layer, False)
                root.addLayer(layer)  # basemap at the bottom, outside the group
            else:
                print("Kunne ikke vise baggrundskortet i QGIS: " + uri)
            continue
        path = os.path.join(folder, "%02d.%s" % (number, "csv" if r.probe.kind == "csv" else "geojson"))
        with open(path, "w", encoding="utf-8") as file:
            file.write(r.text)
        if r.probe.kind == "csv":
            uri = "file://%s?type=csv&delimiter=%%3B&detectTypes=no&geomType=none" % path
            layer = QgsVectorLayer(uri, r.probe.name, "delimitedtext")
            statbank = layer
        else:
            layer = QgsVectorLayer(path, r.probe.name, "ogr")
            if r.probe.url.endswith(KOMMUNER_FILE):
                kommuner = layer
        if not layer.isValid():
            print("QGIS kunne ikke åbne " + r.probe.name)
            continue
        project.addMapLayer(layer, False)
        section.addLayer(layer)

    if kommuner and statbank:
        join = QgsVectorLayerJoinInfo()
        join.setJoinLayer(statbank)
        join.setJoinFieldName(statbank.fields()[0].name())  # OMRÅDE
        join.setTargetFieldName("lau1vaerdi")
        join.setPrefix("statbank_")
        join.setUsingMemoryCache(True)
        kommuner.addJoin(join)
        print("Statbank er koblet på Kommunegrænser (lau1vaerdi = %s)." % statbank.fields()[0].name())

    denmark = QgsRectangle(8.0, 54.5, 15.2, 57.8)
    transform = QgsCoordinateTransform(QgsCoordinateReferenceSystem("EPSG:4326"), project.crs(), project)
    iface.mapCanvas().setExtent(transform.transformBoundingBox(denmark))
    iface.mapCanvas().refresh()


def main(location):
    print("Læser %s" % location)
    probes = probes_from_skill(read_skill(location))
    results = []
    for probe in probes:
        print("Henter %s / %s …" % (probe.section, probe.name), file=sys.stderr)
        results.append(run(probe))
    print(report(results))
    return results


try:
    from qgis.utils import iface as _iface
except ImportError:
    _iface = None

if _iface is not None:
    load_into_qgis(main(default_skill_location()))
elif __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else default_skill_location())
