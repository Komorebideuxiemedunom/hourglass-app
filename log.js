// Hourglass web : carnet d'heures de conduite à imprimer. Les exigences par État sont dans les
// <option> du sélecteur (générées par tools/states.py) ; tout se fait dans le navigateur.
(function () {
  "use strict";
  const esc = (v) => String(v).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  function build() {
    const opt = document.getElementById("logState").selectedOptions[0];
    const name = document.getElementById("student").value.trim();
    const rows = parseInt(document.getElementById("rows").value, 10) || 40;
    const total = opt && opt.value ? Number(opt.dataset.total) : 0, night = opt && opt.value ? Number(opt.dataset.night) : 0;
    const goal = opt && opt.value
      ? `${esc(opt.textContent)} requirement: ${opt.dataset.none ? `no minimum (${total} hours recommended)` : `${total} hours`}${night ? `, including ${night} at night` : ""}.`
      : "Requirement: ______ hours, including ______ at night.";
    const line = (i) => `<tr><td>${i}</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>`;
    document.getElementById("sheet").innerHTML =
      `<h2>Supervised driving log${opt && opt.value ? ` · ${esc(opt.textContent)}` : ""}</h2>` +
      `<p class="goal">${goal}</p>` +
      `<div class="who"><span>Student: <b>${name ? esc(name) : "&nbsp;"}</b></span><span>Permit number: <b>&nbsp;</b></span><span>Permit date: <b>&nbsp;</b></span></div>` +
      `<table><thead><tr><th>#</th><th>Date</th><th>Start</th><th>End</th><th>Minutes</th><th>Night min.</th><th>Road, weather, skills</th><th>Supervisor initials</th></tr></thead>` +
      `<tbody>${Array.from({ length: rows }, (_, i) => line(i + 1)).join("")}</tbody>` +
      `<tfoot><tr><td colspan="4">Totals</td><td></td><td></td><td colspan="2"></td></tr></tfoot></table>` +
      `<div class="sign"><span>Parent or guardian signature: <b>&nbsp;</b></span><span>Date: <b>&nbsp;</b></span></div>` +
      `<p class="small">Night = between sunset and sunrise. Check your state's official form: some DMVs require their own. Printed from Hourglass · komorebideuxiemedunom.github.io/hourglass-app</p>`;
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("logForm").addEventListener("submit", (e) => e.preventDefault());
    document.querySelectorAll("#logForm input, #logForm select").forEach((el) => el.addEventListener("input", build));
    document.getElementById("print").addEventListener("click", () => window.print());
    build();
  });
})();
