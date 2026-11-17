// Router sederhana: tombol .nav-item[data-page] -> App.pages[id].mount(el)
App.router = {
  current: null,
  go(id) {
    const page = App.pages[id];
    if (!page) return console.error("Halaman tidak ada:", id);
    const el = document.getElementById("content");
    el.innerHTML = "";
    this.current = id;
    document.querySelectorAll(".nav-item").forEach((b) =>
      b.classList.toggle("active", b.dataset.page === id));
    page.mount(el);
  },
  init() {
    document.querySelectorAll(".nav-item").forEach((b) =>
      b.addEventListener("click", () => this.go(b.dataset.page)));
  },
};
