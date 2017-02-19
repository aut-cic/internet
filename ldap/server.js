const ldap = require('ldapjs');
const authorize = require('./authorize');
const bind = require('./bind');
const search = require('./search');

function createServer(opts = {}) {
    // Create new ldap server instance
    const server = ldap.createServer();

    // Register bind handler
    server.bind('', bind);

    // Register search handler
    server.search('', authorize, bind);

    // Start listening
    server.listen(opts.port || 1389, function () {
        console.log('LDAP server listening at %s', server.url);
    });
}

module.exports = createServer;