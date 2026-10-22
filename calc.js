// Hourglass web: how much supervised driving is left, and at what pace. Computed in the browser.
// Same requirements as the app (Hourglass/Model/Goal.swift, GoalPresets): keep them aligned.
(function () {
  "use strict";
  const STATES = [{"id": "al", "name": "Alabama", "total": 50.0, "night": 0.0, "months": 6, "note": ""}, {"id": "az", "name": "Arizona", "total": 30.0, "night": 10.0, "months": 6, "note": ""}, {"id": "ca", "name": "California", "total": 50.0, "night": 10.0, "months": 6, "note": ""}, {"id": "co", "name": "Colorado", "total": 50.0, "night": 10.0, "months": 12, "note": ""}, {"id": "fl", "name": "Florida", "total": 50.0, "night": 10.0, "months": 12, "note": ""}, {"id": "ga", "name": "Georgia", "total": 40.0, "night": 6.0, "months": 12, "note": ""}, {"id": "il", "name": "Illinois", "total": 50.0, "night": 10.0, "months": 9, "note": ""}, {"id": "in", "name": "Indiana", "total": 50.0, "night": 10.0, "months": 6, "note": ""}, {"id": "ky", "name": "Kentucky", "total": 60.0, "night": 10.0, "months": 6, "note": ""}, {"id": "la", "name": "Louisiana", "total": 50.0, "night": 15.0, "months": 6, "note": ""}, {"id": "md", "name": "Maryland", "total": 60.0, "night": 10.0, "months": 9, "note": ""}, {"id": "ma", "name": "Massachusetts", "total": 40.0, "night": 0.0, "months": 6, "note": ""}, {"id": "mi", "name": "Michigan", "total": 50.0, "night": 10.0, "months": 6, "note": ""}, {"id": "mn", "name": "Minnesota", "total": 50.0, "night": 15.0, "months": 6, "note": ""}, {"id": "mo", "name": "Missouri", "total": 40.0, "night": 10.0, "months": 6, "note": ""}, {"id": "ny", "name": "New York", "total": 50.0, "night": 15.0, "months": 6, "note": ""}, {"id": "nc", "name": "North Carolina", "total": 60.0, "night": 10.0, "months": 12, "note": ""}, {"id": "oh", "name": "Ohio", "total": 50.0, "night": 10.0, "months": 6, "note": ""}, {"id": "pa", "name": "Pennsylvania", "total": 65.0, "night": 10.0, "months": 6, "note": "Includes 5 hours in bad weather."}, {"id": "sc", "name": "South Carolina", "total": 40.0, "night": 10.0, "months": 6, "note": ""}, {"id": "tn", "name": "Tennessee", "total": 50.0, "night": 10.0, "months": 6, "note": ""}, {"id": "tx", "name": "Texas", "total": 30.0, "night": 10.0, "months": 6, "note": ""}, {"id": "ut", "name": "Utah", "total": 40.0, "night": 10.0, "months": 6, "note": ""}, {"id": "va", "name": "Virginia", "total": 45.0, "night": 15.0, "months": 9, "note": ""}, {"id": "wa", "name": "Washington", "total": 50.0, "night": 10.0, "months": 6, "note": ""}];
  const FR = { aac: { km: 3000, months: 12 }, supervisee: { km: 1000, months: 3 } };
  const $ = (id) => document.getElementById(id);
  const num = (id) => Math.max(0, parseFloat(String($(id).value).replace(",", ".")) || 0);
  const weeksUntil = (iso) => { if (!iso) return null; const d = (new Date(iso + "T12:00:00") - new Date()) / 86400000; return d / 7; };

  function us() {
    const st = STATES.find((s) => s.id === $("state").value) || STATES[0];
    const left = Math.max(st.total - num("done"), 0), nightLeft = Math.max(st.night - num("night"), 0);
    const f = (v) => new Intl.NumberFormat("en-US", { maximumFractionDigits: 1 }).format(v);
    const w = weeksUntil($("test").value);
    let pace = "";
    if (w !== null) pace = w <= 0 ? "<p class='warn'>That date has passed: pick a future test date.</p>" : left > 0 ? `<p>To be ready by then: about <strong>${f(left / w)} hours a week</strong>${nightLeft > 0 ? `, including ${f(nightLeft / w)} at night` : ""}.</p>` : "";
    $("result").innerHTML = `<p class="big">${left > 0 ? `<strong>${f(left)} hours</strong> left${nightLeft > 0 ? `, including <strong>${f(nightLeft)} at night</strong>` : ""}` : "<strong>Hours requirement met.</strong> Check the other conditions below."}</p>
      <p>${st.name}: ${f(st.total)} supervised hours${st.night ? `, ${f(st.night)} at night` : ""}, and at least ${st.months} months with the permit.${st.note ? " " + st.note : ""}</p>${pace}`;
  }

  function fr() {
    const g = FR[$("formule").value];
    const left = Math.max(g.km - num("km"), 0);
    const f = (v) => new Intl.NumberFormat("fr-FR", { maximumFractionDigits: 0 }).format(v);
    let out = `<p class="big">${left > 0 ? `<strong>${f(left)} km</strong> restants sur ${f(g.km)}` : "<strong>Les kilomètres sont faits.</strong>"}</p>`;
    const start = $("debut").value;
    if (start) {
      const min = new Date(start + "T12:00:00"); min.setMonth(min.getMonth() + g.months);
      out += `<p>Durée minimale : ${g.months} mois, donc examen possible à partir du <strong>${min.toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" }).replace(/^1 /, "1er ")}</strong>.</p>`;
      const target = $("examen").value;
      if (target && new Date(target + "T12:00:00") < min) out += `<p class="warn">La date visée tombe avant la fin de la durée minimale.</p>`;
    }
    const w = weeksUntil($("examen").value);
    if (w !== null && left > 0) out += w <= 0 ? `<p class="warn">Choisis une date d'examen à venir.</p>` : `<p>Pour être prêt à temps : environ <strong>${f(left / w)} km par semaine</strong>.</p>`;
    $("result").innerHTML = out;
  }

  document.addEventListener("DOMContentLoaded", () => {
    const run = document.body.dataset.mode === "fr" ? fr : us;
    if ($("state")) $("state").innerHTML = STATES.map((s) => `<option value="${s.id}"${s.id === (document.body.dataset.state || "ca") ? " selected" : ""}>${s.name}</option>`).join("");
    $("calc").addEventListener("submit", (e) => e.preventDefault());
    $("calc").querySelectorAll("input, select").forEach((el) => el.addEventListener("input", run));
    run();
  });
})();
