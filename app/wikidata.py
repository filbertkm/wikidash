from re import I
import requests
from geojson import Point, Feature, FeatureCollection

class SparqlClient:

  def __init__(self):
    self.endpoint = 'https://query.wikidata.org/sparql'

  def query(self, sparql):
    response = requests.get(
      self.endpoint,
      {
        "query": sparql,
        "format": "json"
      }
    )
    data = response.json()
    return data["results"]["bindings"]

  def items_located_in(self, instance_of, located_in):
    sparql = sparql = """
SELECT DISTINCT ?item ?name ?coord ?lat ?lon
WHERE
{
 hint:Query hint:optimizer "None" .
 ?item wdt:P131* wd:#located_in# .
 ?item wdt:P31/wdt:P279* wd:#instance_of# .
 ?item wdt:P625 ?coord .
 ?item p:P625 ?coordinate .
 ?coordinate psv:P625 ?coordinate_node .
 ?coordinate_node wikibase:geoLatitude ?lat .
 ?coordinate_node wikibase:geoLongitude ?lon .
 SERVICE wikibase:label {
 bd:serviceParam wikibase:language "en" .
 ?item rdfs:label ?name
 }
}
ORDER BY ASC (?name)
"""
    sparql = sparql.replace('#located_in#', located_in)
    sparql = sparql.replace('#instance_of#', instance_of)

    return self.query(sparql)

  def item_to_feature(self, item):
    point = Point((float(item["lon"]["value"]), float(item["lat"]["value"])))
    feature = Feature(geometry=point)
    return feature

  def to_geojson(self, instance_of, located_in):
    results = self.items_located_in(instance_of, located_in)

    if len(results) == 0:
      return []

    features = list(map(lambda item: self.item_to_feature(item), results))
    return FeatureCollection(features)

