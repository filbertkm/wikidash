const TILE_SRC_OSM = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const TILE_SRC_WMF = "https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}@1.5x.png?lang=en"

var map = L.map("map").setView([40.7131216, -74.00677], 14);

var tiles = L.tileLayer(TILE_SRC_OSM, {
  maxZoom: 19,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

var myStyle = {
  radius: 8,
  fillColor: "#ff7800",
  color: "#000",
  weight: 1,
  opacity: 1,
  fillOpacity: 0.8,
};

fetch("/instance/Q33506/Q60.geojson")
  .then((response) => response.json())
  .then((data) => {
    const geojsonLayer = L.geoJson(data, {
      style: myStyle,
    });
    geojsonLayer.addTo(map);
    map.fitBounds(geojsonLayer.getBounds());
  });