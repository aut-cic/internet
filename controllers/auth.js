const Controller = require('bak/lib/controller');
const auth = require('../lib/auth');

const Config = require('config');
const {jwt_sign} = require('bak/lib/helpers/security');

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

            let token = jwt_sign(user._id, auth_secret);

            reply.redirect('/status').state('token', id_token, {isSecure: false});

            // reply.view('redirect', {
            //     user,
            //     token,
            //     dst,
            // }).state('token', id_token, {isSecure: false});
        });
    }

    async logout_$$all(request, reply, {all}) {
        await request.user.logout(all ? null : request.session);

        reply.redirect('/').unstate('token', {isSecure: false});
    }

};