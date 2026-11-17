App.pages.home = {
  title: "Beranda",
  mount(el) {
    el.innerHTML = `
      <h1>Beranda</h1>
      <div class="card">
        <h2>Selamat datang</h2>
        <p class="muted">Ini halaman contoh dari starter Eel. Ganti isinya dengan fitur aplikasimu.</p>
        <button class="btn" id="btn-toast">Uji toast</button>
      </div>`;
    el.querySelector("#btn-toast").onclick = () => App.toast("Toast berjalan", "success");
  },
};
