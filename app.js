const Config = require('config');
const {init} = require('bak');

// Bak & Hapi plugins
const MongoosePlugin = require('bak/lib/mongoose');
const LoggingPlugin = require('bak/lib/logging');
const ViewPlugin = require('bak/lib/view');
const AuthPlugin = require('bak/lib/auth');
const RatelimitPlugin = require('bak/lib/ratelimit');

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

        // View
        {register: ViewPlugin, options: {staticCache: 300 * 60 * 1000}},

        // Rate Limiter
        {register: RatelimitPlugin, options: {driver: 'memory'}},
    ],

    routes: [
        require('./controllers/auth'),
        require('./controllers/site'),
    ]

});