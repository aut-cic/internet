const Config = require('config');
const User = require('../models/user');
const {jwt_verify} = require('bak/lib/helpers/security');

const auth_secret = Config.get('auth.secret');

async function auth(username, password) {
    let session_id = await jwt_verify(password, auth_secret);

    if (!session_id) {
        return false;
    }

    let user = await User.findOne({id: username});

    let session = user.sessions.id(session_id);

    if (!session) {
        return false;
    }

    return {user, session};
}

module.exports = auth;