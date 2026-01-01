let map;
let heatmap;

async function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 28.6139, lng: 77.2090 },
    zoom: 11,
    mapTypeId: "roadmap",
  });

  loadHeatmapFromBackend();
}

async function loadHeatmapFromBackend() {
  const res = await fetch("http://127.0.0.1:8000/hotspots");
  const points = await res.json();

  const heatmapData = points.map(p => ({
    location: new google.maps.LatLng(p.lat, p.lng),
    weight: p.weight,
  }));

  heatmap = new google.maps.visualization.HeatmapLayer({
    data: heatmapData,
    radius: 45,
    opacity: 0.75,
  });

  heatmap.setMap(map);
}

window.initMap = initMap;
