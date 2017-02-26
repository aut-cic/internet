const Config = require('config');
const {init} = require('bak');

// Bak & Hapi plugins
const MongoosePlugin = require('bak/lib/mongoose');
const LoggingPlugin = require('bak/lib/logging');
const AuthPlugin = require('bak/lib/auth');
const VisionPlugin = require('vision');
const InertPlugin = require('inert');

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

        // Vision
        {register: VisionPlugin, options: {}},

        // Inert
        {register: InertPlugin, options: {}},
    ],
    routes: [
        require('./controllers/auth'),
        require('./controllers/captiveportal'),
    ]
}).then(({hapi}) => {

    hapi.views({
        engines: {ejs: require('ejs')},
        path: __dirname + '/resources/views'
    });

    hapi.route({
        method: 'GET',
        path: '/static/{param*}',
        config:{
            auth: false,
        },
        handler: {
            directory: {
                path: __dirname + '/resources/static'
            }
        }
    });

});