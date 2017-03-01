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

        const status = await this._usage(request);

        if (status) {
            return reply.redirect('/status');
        }

        if (request.user) {
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
            username: request.user ? request.user.id : null,
            ip: request.ip,
        });
    }

    async status(request, reply) {
        const status = await this._usage(request);

        const {logout} = request.query;

        if (!status) {
            return reply.redirect('/').unstate('token', {isSecure: false});
        }

        reply.view('status', {
            username: request.user ? request.user.username : null,
            group: request.user ? request.user.group : status.group,
            auth: !!request.user,
            ip: request.ip,
            status,
            logout,
        });
    }

    async status_logout_$$ip(request, reply, {ip}) {

        const status = await this._usage(request);

        if (!status) {
            return reply.redirect('/')
                .unstate('token', {isSecure: false});
        }

        await user_logout({
            username: status.username,
            ip: ip || request.ip,
        });

        // If self logging out
        if (!ip || ip === request.ip) {
            if (request.user) {
                await request.user.logout(request.session);
                return reply.redirect('https://internet.aut.ac.ir')
                    .unstate('token', {isSecure: false});
            }
            // // Else direct microtic logout
            // return reply.redirect('https://login.aut.ac.ir/logout')
            //     .unstate('token', {isSecure: false});
        }

        return reply.redirect('/status?logout=' + (ip || request.ip));
    }


};