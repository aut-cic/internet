import http from "k6/http";
import { check, group } from "k6";

const baseURL = "http://127.0.0.1:8080";

export default function () {
  group("status", () => {
    let res = http.get(`${baseURL}/status`);

    check(res, {
      success: (res) => res.status == 200,
      'verify username': (res) => res.body.includes('parham.alvani')
    });
  });
}
