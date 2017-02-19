// http://ldapjs.org/server.html#bind

function bind(req, res, next) {
    let password = req.credentials;
    let username = req.dn.toString();

    console.log('bind', {username, password});

    res.end();
}

module.exports = bind;