// https://acct.aut.ac.ir:8000/api/v1/userusage/?username=s-asadi

const Axios = require('axios');

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

async function logout_session(sid, uid) {
    return Axios.post('/sessions/logout', {
        sid,
        uid
    });
}

async function user_usage(username) {
    let url = 'https://acct.aut.ac.ir:8000/api/v1/userusage/?username=' + username;
    let response;

    try {
        response = await Axios.get(url).then(res => res.data);
    } catch (e) {
        console.error(e);
        return null;
    }

    // const status = {};
    //
    // for (let type of ['daily', 'weekly', 'monthly']) {
    //     p[type] = {
    //         usage: response.usage[type],
    //         total: response.package[type],
    //     }
    // }

    return response
}

module.exports = {
    user_usage
};