const Auth = require('@bakjs/auth')
const {Schema} = require('@bakjs/mongo')

class User extends Auth.User {

    static get $visible() {
        return ['_id', 'name', 'email', 'username', 'group']
    }

    static get $schema() {
        return Object.assign({
            group: {type: String},
            id: {type: String}

        }, Auth.User.$schema)
    }

}

module.exports = User.$model
