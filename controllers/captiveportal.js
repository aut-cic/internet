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

        reply.view(request.query.old ? 'old' : 'index');
    }

    async help(request, reply) {
        reply.view('help');
    }

    async sessions_logout_sid(request, reply, {sid}) {


    }

    async status(request, reply) {
        // if (!request.user) {
        //     return reply.redirect('/');
        // }

        let status;

        try {
            status = await user_usage({
                username: request.user ? request.user.username : null,
                ip: request.ip,
            });
        } catch (e) {
            return reply({error: e, ip: request.ip});
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