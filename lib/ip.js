const IP = require('ip');
const DB = require('./ip_db');

DB.forEach(row => {
    let ip = row.ip;

    if (ip.indexOf('/') === -1) {
        ip += '/24';
    }

    row.subnet = IP.cidrSubnet(ip);
});

function lookupIP(ip) {
    for (let i = 0; i < DB.length; i++) {
        if (DB[i].subnet.contains(ip)) {
            return DB[i];
        }
    }

    return null;
}

module.exports = {
    lookupIP
};