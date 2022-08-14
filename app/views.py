from app import app, wikidata
from flask import jsonify

@app.route("/")
def index():
  return instance_of('Q33506', 'Q60', 'geojson')

@app.route("/instance/<instance>/<location>", defaults={'format':'json'})
@app.route("/instance/<instance>/<location>.<format>")
def instance_of(instance, location, format):
  client = wikidata.SparqlClient()
  if format == 'geojson':
    data = client.to_geojson(instance, location)
  else:
    data = client.items_located_in(instance, location)

  return jsonify(data)