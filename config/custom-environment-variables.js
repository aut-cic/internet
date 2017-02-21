module.exports = {

    mongo: {
        connections: {
            default: {uri: 'MONGO_CONNECTIONS_DEFAULT'},
        }
    },

    auth: {
        secret: 'AUTH_SECRET',
        client: {
            client_secret: 'AUTH_CLIENT_SECRET',
            redirect_uri: 'AUTH_REDIRECT_URI',
        }
    },

    log: {
        sentry: {
            dsn: 'SENTRY_DSN',
        },
    },


};