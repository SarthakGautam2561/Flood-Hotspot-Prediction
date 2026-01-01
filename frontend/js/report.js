let map;
let marker = null;
let severity = null;

function initMap() {
  const delhi = { lat: 28.6139, lng: 77.2090 };

  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 11,
    center: delhi,
  });

  map.addListener("click", (e) => {
    if (marker) marker.setMap(null);
    marker = new google.maps.Marker({
      position: e.latLng,
      map: map,
    });
  });
}

function setSeverity(val) {
  severity = val;
  document.querySelectorAll(".severity button").forEach(b => b.classList.remove("active"));
  document.querySelector(`.severity button:nth-child(${val})`).classList.add("active");
}

async function submitReportForm() {
  if (!marker) {
    alert("Please select location on map");
    return;
  }

  const severity = document.querySelector(".severity button.active")?.innerText;

  if (!severity) {
    alert("Please select severity");
    return;
  }

  const payload = {
    lat: marker.getPosition().lat(),
    lng: marker.getPosition().lng(),
    severity: Number(severity)
  };

  await fetch("http://127.0.0.1:8000/report", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  alert("Report submitted successfully!");
}


window.onload = initMap;
