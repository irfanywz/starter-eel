// Pemanggil API Python. SATU-SATUNYA tempat yang menyentuh `eel.*`.
// Python membalas { ok, data } atau { ok:false, error }.
App.api = {
  async call(name, ...args) {
    const fn = window.eel && window.eel[name];
    if (!fn) throw new Error("API tidak ditemukan: " + name);
    let res;
    try {
      res = await fn(...args)();
    } catch (e) {
      App.toast("Koneksi ke aplikasi terputus", "error");
      throw e;
    }
    if (!res || !res.ok) {
      const msg = (res && res.error) || "Terjadi kesalahan";
      App.toast(msg, "error");
      throw new Error(msg);
    }
    return res.data;
  },
};
