// LDAP Server
// require('./ldap');

module.exports = {
    // Routes
    routes: [
        // './controllers/auth',
        './controllers/site'
    ],

    // Plugins
    registrations: [
        '@bakjs/mongo',
        '@bakjs/logging',
        // '@bakjs/auth',
        '@bakjs/nunjucks',
    ],

    // Plugin options
    auth: {
        user_model: require('./models/user')
    }
}