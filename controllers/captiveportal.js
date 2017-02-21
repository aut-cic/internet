const Controller = require('bak/lib/controller');
const auth = require('../lib/auth');

const Config = require('config');
const {jwt_sign} = require('bak/lib/helpers/security');

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

        reply.view('index');
    }

    async status(request, reply) {
        if (!request.user) {
            return reply.redirect('/');
        }

        reply.view('status', {
            user: request.user,
        });
    }


};