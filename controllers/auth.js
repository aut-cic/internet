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
        this.hapi.inject('/api/oauth/aut/login', ({result}) => {
            let url = result.redirect_uri;
            if (dst) {
                url += '/' + new Buffer(dst).toString('base64');
            }
            reply.redirect(url);
        })
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

        console.log("REQ");
        this.hapi.inject(`/api/oauth/aut/authorize?code=${code}&state=${state}`, ({result}) => {
            let {id_token, user} = result;
            console.log("DONE");
            if (!id_token || !user) {
                return reply.redirect('/');
            }

            // Sign smaller token
            let jwt = jwt_decode(id_token);
            let token = jwt_sign(jwt.s, auth_secret);

            reply.view('redirect', {
                dst,
                username: user.id,
                password: token,
                user,
            }).state('token', id_token, {isSecure: false});
        });
    }

    async logout_$$all(request, reply, {all}) {
        await request.user.logout(all ? null : request.session);

        reply.redirect('/').unstate('token', {isSecure: false});
    }

};