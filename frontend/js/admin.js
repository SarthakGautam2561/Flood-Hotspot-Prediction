async function initAdminMap() {
  const delhi = { lat: 28.6139, lng: 77.2090 };

  const map = new google.maps.Map(document.getElementById("admin-map"), {
    center: delhi,
    zoom: 11,
  });

  // Heatmap from backend
  const res = await fetch("http://127.0.0.1:8000/hotspots");
  const points = await res.json();

  const heatmapData = points.map(p => ({
    location: new google.maps.LatLng(p.lat, p.lng),
    weight: p.weight,
  }));

  const heatmap = new google.maps.visualization.HeatmapLayer({
    data: heatmapData,
    radius: 40,
    opacity: 0.75,
  });

  heatmap.setMap(map);
}

async function loadDashboardData() {
  /* ===== SUMMARY CARDS ===== */
  const summaryRes = await fetch("http://127.0.0.1:8000/data/summary");
  const summary = await summaryRes.json();

  document.getElementById("totalReports").innerText = summary.total_reports;
  document.getElementById("highRisk").innerText = summary.high_risk;
  document.getElementById("mediumRisk").innerText = summary.medium_risk;
  document.getElementById("responseRate").innerText =
    summary.response_rate + "%";

  /* ===== RECENT REPORTS ===== */
  const recentRes = await fetch("http://127.0.0.1:8000/data/recent");
  const recent = await recentRes.json();

  const recentCard = document.querySelector(
    ".card strong + .recent-item"
  )?.parentElement;

  if (!recentCard) return;

  // Remove old static items
  recentCard.querySelectorAll(".recent-item").forEach(el => el.remove());

  recent.forEach(r => {
    const item = document.createElement("div");
    item.className = "recent-item";

    const riskClass =
      r.severity >= 4 ? "high" :
      r.severity === 3 ? "medium" : "low";

    item.innerHTML = `
      <span>Reported Location</span>
      <div class="status ${riskClass}"></div>
      <small>${new Date(r.time).toLocaleTimeString()}</small>
    `;

    recentCard.appendChild(item);
  });
}

window.onload = () => {
  initAdminMap();
  loadDashboardData();
};

async function loadWardTable() {
  const res = await fetch("http://127.0.0.1:8000/data/ward-risk");
  const data = await res.json();

  const tbody = document.getElementById("ward-table-body");
  tbody.innerHTML = "";

  data.forEach(row => {
    const riskClass =
      row.risk === "High" ? "high" :
      row.risk === "Medium" ? "medium" : "low";

    tbody.innerHTML += `
      <tr>
        <td data-label="Ward / Area">${row.ward}</td>
        <td data-label="Zone">${row.zone}</td>
        <td data-label="Risk Level">
          <span class="pill ${riskClass}">${row.risk}</span>
        </td>
        <td data-label="Reports">${row.reports}</td>
        <td data-label="Updated">${row.updated}</td>
      </tr>
    `;
  });
}

document.addEventListener("DOMContentLoaded", loadWardTable);
