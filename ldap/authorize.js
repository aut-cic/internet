function authorize(req, res, next) {

    console.log('authorize', req.connection.ldap.bindDN);

    if (!req.connection.ldap.bindDN.equals('cn=root'))
        return next(new ldap.InsufficientAccessRightsError());

    return next();
}

module.exports = authorize;