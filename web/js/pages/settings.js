App.pages.settings = {
  title: "Pengaturan",
  mount(el) {
    const theme = App.state.settings.theme;
    el.innerHTML = `
      <h1>Pengaturan</h1>
      <div class="card">
        <div class="row">
          <div><strong>Tema</strong><div class="muted">Gelap atau terang</div></div>
          <button class="btn secondary" id="btn-theme">${theme === "dark" ? "Gelap" : "Terang"}</button>
        </div>
        <div class="row">
          <div><strong>Folder data</strong><div class="muted">Tempat semua data aplikasi disimpan</div></div>
          <button class="btn secondary" id="btn-data">Buka</button>
        </div>
      </div>`;

    el.querySelector("#btn-theme").onclick = async (e) => {
      const next = App.state.settings.theme === "dark" ? "light" : "dark";
      App.state.settings = await App.api.call("settings_set", "theme", next);
      App.applyTheme();
      e.target.textContent = next === "dark" ? "Gelap" : "Terang";
    };
    el.querySelector("#btn-data").onclick = () => App.api.call("app_open_data_dir");
  },
};
