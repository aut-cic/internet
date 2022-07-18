import { Controller } from "bak";
const { user_usage } = require("../lib/acct");
const { lookupIP, updateDB } = require("../lib/ip");
const MESSAGES = require("../lib/messages");

export default class SiteController extends Controller {
  constructor() {
    super({
      default: {
        plugins: {
          ratelimit: {
            limit: 5,
            duration: 60 * 1000,
          },
        },
      },
    });
  }

  async _(request, reply) {
    const dst = request.query.dst;

    const error = request.query.error;

    const status = await this._usage(request);

    const external = false; //request.ip.indexOf('192') !== 0 && request.ip.indexOf('172') !== 0;

    if (status || request.user) {
      return reply.redirect("/status");
    }

    reply.view("index", {
      dst,
      error,
      external,
      announcements,
      MESSAGES: MESSAGES[request.query.lang || "fa"],
      dir: request.query.lang === "en" ? "ltr" : "rtl",
      otherLang: {},
    });
  }

  _usage(request) {
    const ip =
      request.ip.indexOf("192") === 0 || request.ip.indexOf("172") === 0
        ? request.ip
        : null;
    return user_usage({
      username: request.user ? request.user.id : null,
      ip,
    });
  }

  async status(request, reply) {
    const status = await this._usage(request);

    let { logout, dst } = request.query;

    if (!status) {
      return reply.redirect("/").unstate("token", { isSecure: false });
    }

    if (
      dst &&
      (dst.indexOf("internet.aut.ac.ir") !== -1 ||
        dst.indexOf("login.aut.ac.ir") !== -1)
    ) {
      dst = null;
    }

    const location = lookupIP(request.ip);

    // History
    const history = {
      labels: [],
      discount: [],
      usage: [],
    };
    status.usageHistory.forEach(({ date, usage, discount }) => {
      history.labels.push(date);
      history.discount.push(discount);
      history.usage.push(usage);
    });

    reply.view("status", {
      username: request.user ? request.user.username : status.username,
      group: request.user ? request.user.group : status.group,
      auth: !!request.user,
      ip: request.ip,
      location: location ? location.description : "-",
      announcements,
      status,
      logout,
      dst,
      history: {
        labels: JSON.stringify(history.labels),
        usage: JSON.stringify(history.usage),
        discount: JSON.stringify(history.discount),
      },
      rand: Math.floor(Math.random() * 1000),
    });
  }

  async ipInfo_lookup_$$ip(request, reply, { ip }) {
    reply(lookupIP(ip || request.ip));
  }

  async ipInfo(request, reply) {
    const subenets = updateDB();
    reply(subenets);
  }
}
