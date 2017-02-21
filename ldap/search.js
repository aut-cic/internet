const User = require('../models/user');

// http://ldapjs.org/server.html#search

async function search(req, res, next) {
    let dn = req.dn.toString();
    let scope = req.scope;
    let filter = req.filter.toString();

    console.log("SEARCH", {dn, filter});

    let username = req.filter.json.value;

    let user = await User.findOne({id: username});

    if (!user) {
        return res.end();
    }

    res.send({
        //dn: 'CN=' + user._id + ',' + req.dn.toString(),
        dn: user._id,
        attributes: Object.assign({
            objectclass: ['organization', 'top'],
        }, user)
    });

    res.end();
}

module.exports = search;