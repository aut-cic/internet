const Controller = require('bak/lib/controller');
const auth = require('../lib/auth');

module.exports = class AuthController extends Controller {

    constructor() {
        super({
            default: {
                auth: false,
            }
        });
    }

    async login(request, reply) {
        let {dst} = request.query || {};
        this.hapi.inject('/api/oauth/aut/login', ({result}) => {
            let url = result.redirect_uri;
            if (dst) {
                url += '/' + new Buffer(dst).toString('base64');
            }
            reply.redirect(url);
        })
    }

    async auth(request, reply) {
        let {token} = request.query || {};
        let user = await auth(token);

        reply({user});
    }

    async authorize_$$dst(request, reply, {dst}) {
        let {code, state} = request.query || {};

        if (dst) {
            try {
                dst = new Buffer(dst, 'base64').toString();
            } catch (e) {
                console.error(e);
                dst = null;
            }
        }

        if (!dst) {
            dst = 'http://aut.ac.ir';
        }

        this.hapi.inject(`/api/oauth/aut/authorize?code=${code}&state=${state}`, ({result}) => {
            let {id_token, user} = result;

            if (!id_token || !user) {
                return reply('Error reported.' + "\r\nIP: " + request.ip);
            }

            reply({
                username: user.email,
                password: id_token,
                dst
            });
        });
    }

};