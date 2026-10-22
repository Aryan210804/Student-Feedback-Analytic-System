const C = { teal: "#0e7c86", ink: "#1b2a41", coral: "#d1495b", green: "#3c8d5a", grey: "#9aa5b4" };

fetch("/api/summary").then(r => r.json()).then(s => {
  const draw = (id, type, labels, data, colors, opts = {}) =>
    new Chart(document.getElementById(id), {
      type,
      data: { labels, datasets: [{ data, backgroundColor: colors, borderColor: colors, borderWidth: type === "line" ? 2 : 0, tension: .3 }] },
      options: { plugins: { legend: { display: type === "doughnut" } }, ...opts }
    });
  const rating = { scales: { y: { min: 0, max: 5 } } };

  draw("cat", "bar", Object.keys(s.categories), Object.values(s.categories), C.teal, rating);
  draw("dist", "bar", Object.keys(s.ratings), Object.values(s.ratings), C.ink);
  draw("sent", "doughnut", Object.keys(s.sentiment), Object.values(s.sentiment),
       Object.keys(s.sentiment).map(k => ({ Positive: C.green, Negative: C.coral, Neutral: C.grey })[k]));
  draw("trend", "line", s.monthly.labels, s.monthly.values, C.teal, { scales: { y: { min: 1, max: 5 } } });
  draw("dept", "bar", s.departments.labels, s.departments.values, C.ink, { indexAxis: "y", scales: { x: { min: 0, max: 5 } } });
});
