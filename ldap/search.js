const User = require('../models/user');

// http://ldapjs.org/server.html#search

async function search(req, res, next) {
    let dn = req.dn.toString();
    let scope = req.scope;
    let filter = req.filter.toString();

    let username = req.filter.json.value;

    console.log("SEARCH", username);

    let user = await User.findOne({id: username});

    if (!user) {
        return res.end();
    }


    res.send({
        dn: 'CN=' + user.get('id'),
        attributes: Object.assign({
            objectclass: ['organization', 'top'],
            memberOf: [user.get('group')],
            real_username: user.get('username'),
            email: user.get('email'),
        }, user)
    });

    res.end();
}

module.exports = function (req, res, next) {
    search(req, res, next).catch((e) => {
        console.error(e);
        res.end();
    })
};