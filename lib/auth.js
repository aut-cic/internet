const Config = require('config');
const User = require('../models/user');
const {jwt_verify} = require('bak/lib/helpers/security');

const auth_secret = Config.get('auth.secret');

async function auth(token) {
    let data = await jwt_verify(token, auth_secret);

    if (!data) {
        return false;
    }

    let user = await User.find(data.i);

    return user;
}

module.exports = auth;