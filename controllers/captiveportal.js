const Controller = require('bak/lib/controller');
const auth = require('../lib/auth');

const Config = require('config');
const {jwt_sign} = require('bak/lib/helpers/security');
const {user_usage} = require('../lib/acct');

const auth_secret = Config.get('auth.secret');

// http://stackoverflow.com/questions/10420352

function humanFileSize(bytes, si) {
    var thresh = si ? 1000 : 1024;
    if (Math.abs(bytes) < thresh) {
        return bytes + ' بایت';
    }
    var units = si
        ? ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        : ['کیلوبایت', 'مگابایت', 'گیگابایت', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
    var u = -1;
    do {
        bytes /= thresh;
        ++u;
    } while (Math.abs(bytes) >= thresh && u < units.length - 1);
    return bytes.toFixed(1) + ' ' + units[u];
}

global.humanFileSize = humanFileSize;

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

        const usage = await user_usage(request.user.username);

        reply.view('status', {
            user: request.user,
            usage,
        });
    }


};