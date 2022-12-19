import "bootstrap/dist/css/bootstrap.rtl.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import "./bootstrap.scss";
import * as bootstrap from "bootstrap/dist/js/bootstrap.min.js";

import "vazirmatn/Vazirmatn-font-face.css";
import "vazirmatn/misc/Farsi-Digits/Vazirmatn-FD-font-face.css";

import "./app.css";
import "./gauge.css";
import "./index.js";
import "./login.ts";

window.console.log("https://github.com/aut-cic/internet");
window.console.log("AUT internet controller frontend and backend");

window.onload = () => {
  let modal = window.document.getElementById("packageModal");
  if (modal != null) {
    let w = new bootstrap.Modal(modal);
    w.show();
    window.console.log("Hello, We have modal");
    setTimeout(() => {
      w.hide();
      w.dispose();
    }, 1500);
  }
};
