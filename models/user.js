const BaseUser = require('bak/lib/auth/user');
const {Schema} = require('mongoose');
const {bcrypt_hash} = require('bak/lib/helpers/security');

class User extends BaseUser {

    static get $visible() {
        return ['_id', 'name', 'email', 'username'];
    }

    static get $schema() {
        return Object.assign({
            // exp: {type: Date, expires: 3600, default: Date.now},

        }, BaseUser.$schema);
    };

}

module.exports = User.$model;
