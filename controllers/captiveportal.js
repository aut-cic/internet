const Controller = require('bak/lib/controller');
const auth = require('../lib/auth');

const Config = require('config');
const {jwt_sign} = require('bak/lib/helpers/security');
const {user_usage} = require('../lib/acct');

const auth_secret = Config.get('auth.secret');

module.exports = class CaptivePortalController extends Controller {

    constructor() {
        super({
            default: {
                auth: {mode: 'try'},
            }
        });
    }

    async _(request, reply) {

        if (request.user) {
            return reply.redirect('/status');
        }

        try {
            let status = await this._usage(request);
            if (status) {
                return reply.redirect('/status');
            }
        } catch (e) {
        }

        reply.view(request.query.old ? 'old' : 'index');
    }

    async help(request, reply) {
        reply.view('help');
    }

    async sessions_logout_sid(request, reply, {sid}) {


    }

    _usage(request) {
        return user_usage({
            username: request.user ? request.user.username : null,
            ip: request.ip,
        });
    }

    async status(request, reply) {
        try {
            var status = await this._usage(request);
        } catch (e) {
            return reply.redirect('/');
            // return reply({error: e, ip: request.ip});
        }

        reply.view('status', {
            username: request.user ? request.user.username : status.username,
            group: request.user ? request.user.group : status.group,
            auth: !!request.user,
            ip: request.ip,
            status,
        });
    }


};