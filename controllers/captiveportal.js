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
        if (!request.user) {
            return reply.redirect('/');
        }

        const status = await user_usage({
            username: request.user.username,
            ip: request.ip,
        });

        reply.view('status', {
            user: request.user,
            ip: request.ip,
            status,
        });
    }


};