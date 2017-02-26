// https://acct.aut.ac.ir:8000/api/v1/userusage/?username=s-asadi

const Axios = require('axios');

async function user_usage(username) {
    let url = 'https://acct.aut.ac.ir:8000/api/v1/userusage/?username=' + username;
    let d = {
        usage: {},
        package: {},
        resetConfig: {},
        sessions: [],
    };
    try {
        d = await Axios.get(url).then(res => res.data);
    } catch (e) {
        console.error(e);

    }
    return d;

    // {
    //     "speeds": {
    //         "PhD-H1": "2M/5M",
    //         "PhD": "12M/25M",
    //         "PhD-H2": "1M/2500K",
    //         "PhD-H3": "625K/625K"
    //     },
    //     "usage": {
    //         "monthly": 7498941330,
    //         "daily": 0,
    //         "weekly": 7498941330
    //     },
    //     "username": "s-asadi",
    //     "package": {
    //         "monthly": 24.0,
    //         "daily": 3.0,
    //         "weekly": 9.0
    //     },
    //     "groupname": "PhD",
    //     "resetConfig": {
    //         "monthly": 1,
    //         "daily": "02:00 AM",
    //         "weekly": 5
    //     },
    //     "sessions": [
    //         {
    //             "framedipaddress": "192.168.36.142",
    //             "acctstarttime": "2017-02-26T00:43:54Z",
    //             "usage": 4582063747,
    //             "acctuniqueid": "903bb851e5f043ff99614df06687c1be",
    //             "acctsessionid": "80200b78"
    //         }
    //     ]
    // };
}

module.exports = {
    user_usage
};