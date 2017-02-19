const Config = require('config');
const {init} = require('bak');

// Bak plugins
const MongoosePlugin = require('bak/lib/mongoose');
const LoggingPlugin = require('bak/lib/logging');
const AuthPlugin = require('bak/lib/auth');

// LDAP Server
require('./ldap');

// App
const UserModel = require('./models/user');

init({
    plugins: [
        // Logging
        {register: LoggingPlugin, options: Config.get('log')},

        // Mongoose
        {register: MongoosePlugin, options: Config.get('mongo')},

        // Auth
        {register: AuthPlugin, options: Object.assign({user_model: UserModel}, Config.get('auth'))},
    ],

    routes: [
        require('./controllers/auth')
    ],

});