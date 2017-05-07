const BaseUser = require('bak/lib/auth/provider/user');
const {Schema} = require('mongoose');

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
