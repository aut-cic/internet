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

    auth: {
        user_model: require('./models/user')
    }

    nunjucks: {
        staticCache: 300 * 60 * 1000 
    }
    
}