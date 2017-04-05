const {Model} = require('bak');
const {Schema} = require('mongoose');
const {bcrypt_hash} = require('bak/lib/helpers/security');

class Subnet extends Model {

    static get $schema() {
        return {
            subnet: {type: "String"},
            description: {type: "String"},
        }
    };

}

module.exports = Subnet.$model;
