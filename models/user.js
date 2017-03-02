const BaseUser = require('bak/lib/auth/user');
const {Schema} = require('mongoose');
const {bcrypt_hash} = require('bak/lib/helpers/security');

class User extends BaseUser {

    static get $visible() {
        return ['_id', 'name', 'email', 'username', 'group'];
    }

    static get $schema() {
        return Object.assign({
            group: {type: String},
            id: {type: String}

        }, BaseUser.$schema);
    };

}

module.exports = User.$model;
