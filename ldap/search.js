// http://ldapjs.org/server.html#search

function search(req, res, next) {
    let dn = req.dn.toString();
    let scope = req.scope;
    let filter = req.filter.toString();

    console.log('search', {dn, scope, filter});

    let obj = {
        dn: 'CN=test50,' + req.dn.toString(),
        attributes: {
            objectclass: ['organization', 'top'],
            samaccountname: 'test50',
        }
    };

    if (req.filter.matches(obj.attributes)) {
        console.log("Match!");
        res.send(obj);
    }

    res.end();
}

module.exports = search;