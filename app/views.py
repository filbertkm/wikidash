from app import app, wikidata
from flask import jsonify, render_template

@app.route("/")
def index():
  return map()

@app.route("/instance/<instance>/<location>", defaults={'format':'json'})
@app.route("/instance/<instance>/<location>.<format>")
def instance_of(instance, location, format):
  client = wikidata.SparqlClient()
  if format == 'geojson':
    data = client.to_geojson(instance, location)
  else:
    data = client.items_located_in(instance, location)

  return jsonify(data)

@app.route("/map")
def map():
  return render_template(
        'map.html',
        title="Wikidata Query Map",
        description="Wikidata Query Map"
    )
