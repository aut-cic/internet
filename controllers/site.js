const Controller = require('bak/lib/controller');
const auth = require('../lib/auth');
const Config = require('config');
const {jwt_sign} = require('bak/lib/helpers/security');
const {user_usage, user_logout} = require('../lib/acct');
const {lookupIP} = require('../lib/ip');
const auth_secret = Config.get('auth.secret');
const {stats} = require('../lib/cache');

module.exports = class SiteController extends Controller {

    constructor() {
        super({
            default: {
                auth: {mode: 'try'},
            }
        });
    }

    async _(request, reply) {

        const dst = request.query.dst;

        const error = request.query.error;

        const status = await this._usage(request);

        const external = request.ip.indexOf('192') !== 0 && request.ip.indexOf('172') !== 0;

        if (status || request.user) {
            return reply.redirect('/status');
        }

        reply.view(request.query.next ? 'index' : 'old', {
            dst,
            error,
            external
        });
    }

    async help(request, reply) {
        reply.view('help');
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

        reply.view('status', {
            username: request.user ? request.user.username : status.username,
            group: request.user ? request.user.group : status.group,
            auth: !!request.user,
            ip: request.ip,
            location: location ? location.description : '-',
            status,
            logout,
            dst
        });
    }

    async ipInfo_$$ip(request, reply, {ip}) {
        reply(lookupIP(ip || request.ip));
    }

    async throwCrash(request, reply) {
        a = 2;
    }

    async cacheStats(request, reply) {
        reply(stats());
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