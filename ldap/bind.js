const ldap = require('ldapjs');
const auth = require('../lib/auth');
const Config = require('config');
// http://ldapjs.org/server.html#bind

const rad_username = Config.get('radius.username');
const rad_password = Config.get('radius.password');

async function bind(req, res, next) {
    const password = req.credentials;

    const username = req.dn.toString().split('cn=')[1].split(',')[0].trim();

    console.log("BIND", username + ':' + password);

    if (username === rad_username && password === rad_password) {
        console.log("RADIUS success login");
        return res.end();
    }

    let user = await auth(username, password);

    if (!user) {
        return next(new ldap.InsufficientAccessRightsError());
    }

    res.end();
}

module.exports = function (req, res, next) {
    bind(req, res, next).catch((e) => {
        console.error(e);
        res.end();
    })
};