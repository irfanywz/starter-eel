App.pages.about = {
  title: "Tentang",
  mount(el) {
    const i = App.state.info;
    el.innerHTML = `
      <h1>Tentang</h1>
      <div class="card">
        <dl class="kv">
          <dt>Aplikasi</dt><dd>${i.name}</dd>
          <dt>Versi</dt><dd>${i.version}</dd>
          <dt>Mode</dt><dd>${i.frozen ? "Build (exe)" : "Development"}</dd>
          <dt>Folder data</dt><dd>${i.data_dir}</dd>
        </dl>
      </div>`;
  },
};
