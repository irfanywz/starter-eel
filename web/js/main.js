// Titik masuk frontend: ambil info + setting dari Python, lalu tampilkan halaman awal.
App.applyTheme = function () {
  document.documentElement.dataset.theme = App.state.settings.theme || "dark";
};

window.addEventListener("error", (e) => App.toast(e.message || "Error", "error"));
window.addEventListener("unhandledrejection", () => {}); // error API sudah di-toast oleh App.api

window.addEventListener("DOMContentLoaded", async () => {
  App.router.init();
  try {
    App.state.info = await App.api.call("app_info");
    App.state.settings = await App.api.call("settings_get_all");
  } catch (e) {
    return;
  }
  App.applyTheme();
  document.title = App.state.info.name;
  document.getElementById("brand").textContent = App.state.info.name;
  document.getElementById("version").textContent = "v" + App.state.info.version;
  App.router.go("home");
});
