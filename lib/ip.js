const IP = require('ip');
const Subnet = require('../models/subnet');
const _subnets = [];

async function updateDB() {
    const subnets = await Subnet.find({});
    _subnets.splice(0);

    subnets.forEach(subnet => {
        let cidr = subnet.subnet;

        if (cidr.indexOf('/') === -1) {
            cidr += '/24';
        }

        subnet.cidr = IP.cidrSubnet(cidr);
        _subnets.push(subnet);
    });

    return _subnets;
}

function lookupIP(ip) {
    for (let i = 0; i < _subnets.length; i++) {
        if (_subnets[i].cidr.contains(ip)) {
            return _subnets[i];
        }
    }
    return null;
}

updateDB().catch(console.err);

module.exports = {
    lookupIP,
    updateDB
};