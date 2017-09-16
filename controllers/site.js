const { Controller } = require('bak');
const auth = require('../lib/auth');
const Config = require('config');
const {user_usage, user_logout} = require('../lib/acct');
const {lookupIP, updateDB} = require('../lib/ip');
const auth_secret = Config.get('auth.secret');
const MESSAGES = require('../lib/messages');
const Announcement = require('../models/announcement');

module.exports = class SiteController extends Controller {

    constructor() {
        super({
            default: {
                // auth: {mode: 'try'},
                plugins: {
                    ratelimit: {
                        limit: 5,
                        duration: 60 * 1000,
                    }
                }
            }
        });
    }

    async _(request, reply) {

        const dst = request.query.dst;

        const error = request.query.error;

        const status = await this._usage(request);

        const external = false;//request.ip.indexOf('192') !== 0 && request.ip.indexOf('172') !== 0;

        const announcements = await Announcement.find({visible: {$ne: false}, login: true});

        if (status || request.user) {
            return reply.redirect('/status');
        }

        reply.view(request.query.next ? 'index' : 'old', {
            dst,
            error,
            external,
            announcements,
            MESSAGES: MESSAGES[request.query.lang || 'fa'],
            dir: request.query.lang === 'en' ? 'ltr' : 'rtl',
            otherLang: {}
        });
    }

    _usage(request) {
        const ip = (request.ip.indexOf('192') === 0 || request.ip.indexOf('172') === 0) ? request.ip : null;
        return user_usage({
            username: request.user ? request.user.id : null,
            ip,
        });
    }

    async status(request, reply) {
        const status = await this._usage(request);

        let {logout, dst} = request.query;

        if (!status) {
            return reply.redirect('/').unstate('token', {isSecure: false});
        }

        if (dst && (dst.indexOf('internet.aut.ac.ir') !== -1 || dst.indexOf('login.aut.ac.ir') !== -1)) {
            dst = null;
        }

        const location = lookupIP(request.ip);

        const announcements = await Announcement.find({visible: {$ne: false}, status: true});

        // History
        const history = {
            labels: [],
            data: [],
            colors: []
        };
        status.usageHistory.forEach(({date, usage, effective}) => {
            history.labels.push(date);
            history.data.push(usage);
            history.colors.push(effective ? 'rgba(54, 162, 235, 0.2)' : 'rgba(255, 99, 132, 0.2)');
        });

        reply.view('status', {
            username: request.user ? request.user.username : status.username,
            group: request.user ? request.user.group : status.group,
            auth: !!request.user,
            ip: request.ip,
            location: location ? location.description : '-',
            announcements,
            status,
            logout,
            dst,
            history: {
                labels: JSON.stringify(history.labels),
                data: JSON.stringify(history.data),
                colors: JSON.stringify(history.colors)
            },
            rand: Math.floor(Math.random() * 1000)
        });
    }

    async ipInfo_lookup_$$ip(request, reply, {ip}) {
        reply(lookupIP(ip || request.ip));
    }

    async ipInfo(request, reply) {
        const subenets = updateDB();
        reply(subenets);
    }

    async status_logout_$$id(request, reply, {id}) {

        const status = await this._usage(request);

        if (!status) {
            return reply.redirect('/').unstate('token', {isSecure: false});
        }

        let session = status.current_session;
        if (id) {
            for (let s of status.sessions) {
                if (s.id === id) {
                    session = s;
                    break;
                }
            }
        }

        await user_logout({
            username: status.username,
            acctuniqueid: session.id,
            ip: session.ip,
        });


        if (request.user) {
            await request.user.logout(request.session);
        }

        return reply.redirect('/').unstate('token', {isSecure: false});
    }


};