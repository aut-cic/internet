const Controller = require('bak/lib/controller');
const auth = require('../lib/auth');

const Config = require('config');
const {jwt_sign, jwt_decode} = require('bak/lib/helpers/security');

const auth_secret = Config.get('auth.secret');


module.exports = class AuthController extends Controller {

    constructor() {
        super({
            default: {
                auth: false,
            },
            routes: {
                logout_$$all: {
                    auth: {mode: 'required'}
                }
            }
        });
    }

    async login(request, reply) {
        let {dst} = request.query || {};

        const auth = this.hapi.plugins['bak-auth'].auth;
        let redirect_uri = await auth.oauth_login('aut');

        if (dst) {
            redirect_uri += '/' + new Buffer(dst).toString('base64');
        }

        reply.redirect(redirect_uri);
    }

    async check(request, reply) {
        let {username, password} = request.query || {};

        if (!username || !password) {
            reply.redirect('/');
        }

        let auth_info = await auth(username, password);
        reply(auth_info);
    }

    async authorize_$$dst(request, reply, {dst}) {
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

        try {
            const auth = this.hapi.plugins['bak-auth'].auth;
            let {id_token, user} = await auth.oauth_authorize('aut', request);

            console.log("AUTH OK For " + user.id);

            // Sign smaller token
            let jwt = jwt_decode(id_token);
            let token = jwt_sign(jwt.s, auth_secret);

            reply.view('redirect', {
                dst,
                username: user.id,
                password: token,
                user,
            }).state('token', id_token, {isSecure: false});

        } catch (e) {
            console.error(e);
            return reply.redirect('/');
        }

    }

};