import "bootstrap-icons/font/bootstrap-icons.css";
// Compiled from source with our palette, then flipped to RTL by postcss/rtlcss.
// Do not add the prebuilt bootstrap.rtl.min.css back alongside it: that ships
// the whole framework a second time.
import "./bootstrap.scss";
import * as bootstrap from "bootstrap/dist/js/bootstrap.min.js";

import "./fonts.css";

import "./app.css";
import "./gauge.css";
// Both read the DOM at module scope, which is safe because the bundle is
// loaded with `defer` (see templates/includes/scripts.html) and therefore runs
// after the document is parsed. Dropping defer would silently break them.
import "./login";
import "./status";

window.console.log("https://github.com/aut-cic/internet");
window.console.log("AUT internet controller frontend and backend");

window.onload = () => {
  const modal = window.document.getElementById("packageModal");
  if (modal != null) {
    const w = new bootstrap.Modal(modal);
    w.show();
    setTimeout(() => {
      w.hide();
    }, 3000);
  }
};
