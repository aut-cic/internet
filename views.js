const Nunjucks = require('nunjucks');
const Vision = require('vision');
const path = require('path');

exports.register = (server, options, next) => {

    const njk = {
        compile: (src, options) => {
            const template = Nunjucks.compile(src, options.environment);
            return function (context) {
                return template.render(context);
            };
        },
        prepare: (options, next) => {
            options.compileOptions.environment = Nunjucks.configure(options.path, {watch: false});
            return next();
        },
    };

    server.register(Vision, () => {
        server.views({
            engines: {njk},
            isCached: process.env.NODE_ENV === 'production',
            path: path.join(__dirname, '/resources/views')
        });
    });

    server.route({
        method: 'GET',
        path: '/static/{param*}',
        config: {
            auth: false,
            cache: {
                expiresIn: 30 * 60 * 1000,
            }
        },
        handler: {
            directory: {
                path: __dirname + '/resources/static'
            }
        }
    });

    if (next) next();
};

exports.register.attributes = {
    name: 'views'
};