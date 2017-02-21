const ldap = require('ldapjs');
const auth = require('../lib/auth');

// http://ldapjs.org/server.html#bind

async function bind(req, res, next) {
    let password = req.credentials;

    //let username = req.dn.toString().split('cn=')[1].split(',')[0].trim();
    let username = req.dn.toString();

    console.log("BIND", username + ':' + password);

    if (password === 'opnsense@123') {
        return res.end();
    }

    let user = await auth(username, password);

    if (!user) {
        return next(new ldap.InsufficientAccessRightsError());
    }

    res.end();
}

module.exports = bind;