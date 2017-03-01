const Controller = require('bak/lib/controller');
const auth = require('../lib/auth');

const Config = require('config');
const {jwt_sign} = require('bak/lib/helpers/security');
const {user_usage, user_logout} = require('../lib/acct');

const auth_secret = Config.get('auth.secret');

module.exports = class StatusController extends Controller {

    constructor() {
        super({
            default: {
                auth: {mode: 'try'},
            }
        });
    }

    async _(request, reply) {

        const dst = request.query.dst || 'https://internet.aut.ac.ir/status';

        const error = request.query.error;

        if (request.user) {
            return reply.redirect('/status');
        }


        let status = await this._usage(request);

        if (status) {
            return reply.redirect('/status');
        }

        reply.view(request.query.next ? 'index' : 'old', {
            dst,
            error
        });
    }

    async help(request, reply) {
        reply.view('help');
    }


    _usage(request) {
        return user_usage({
            username: request.user ? request.user.username : null,
            ip: request.ip,
        });
    }

    async status(request, reply) {
        const status = await this._usage(request);

        if(!status) {
            return reply.redirect('/');
        }

        reply.view('status', {
            username: request.user ? request.user.username : status.username,
            group: request.user ? request.user.group : status.group,
            auth: !!request.user,
            ip: request.ip,
            status,
        });
    }

    async status_logout_$$ip(request, reply, {ip}) {
        await user_logout({
            username: request.user ? request.user.username : null,
            ip: ip || request.ip,
        });

        if (request.user && (!ip || ip === request.ip)) {
            await request.user.logout(request.session);
            return reply.redirect('https://internet.aut.ac.ir')
                .unstate('token', {isSecure: false});
        }

        return reply.redirect('/status');
    }


};