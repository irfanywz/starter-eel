// App.toast("pesan", "info" | "success" | "error", durasiMs)
App.toast = function (message, type = "info", ms = 2600) {
  const wrap = document.getElementById("toast-wrap");
  const el = document.createElement("div");
  el.className = "toast " + type;
  el.textContent = message;
  wrap.appendChild(el);
  setTimeout(() => el.remove(), ms);
};
