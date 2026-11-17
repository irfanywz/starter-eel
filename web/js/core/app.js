// Namespace global tunggal. Semua modul JS menempel ke window.App.
window.App = {
  pages: {},     // diisi oleh js/pages/*.js  -> App.pages.<id> = { title, mount(el) }
  state: {       // state global ringan
    settings: {},
    info: {},
  },
};
