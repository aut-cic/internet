module.exports = {

    mongo: {
        connections: {
            default: {uri: 'MONGO_CONNECTIONS_DEFAULT'},
        }
    },

    radius: {
        username: 'RADIUS_USERNAME',
        password: 'RADIUS_PASSWORD'
    },

    auth: {
        secret: 'AUTH_SECRET',
        oauth: {
            aut: {
                client_id: 'AUTH_CLIENT_ID',
                redirect_uri: 'AUTH_REDIRECT_URI',
                client_secret: 'AUTH_CLIENT_SECRET',
            }
        },
    },

    log: {
        sentry: {
            dsn: 'SENTRY_DSN',
        },
    },


};