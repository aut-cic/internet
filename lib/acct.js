const Axios = require('axios');

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

// Create axios instance
const _acct = Axios.create({
    baseURL: process.env.ACCT_URL || 'https://acct.aut.ac.ir:8000',
});

async function user_usage({username, ip}) {

    let response;

    // try {
    //     response = await _acct.get('api/v1/userusage', {params: {username, ip}}).then(res => res.data);
    // } catch (e) {
    //     console.error(e);
    // }

    response = response || {
            "speeds": {
                "PhD-H1": "2M/5M",
                "PhD": "12M/25M",
                "PhD-H2": "1M/2500K",
                "PhD-H3": "625K/625K"
            },
            "usage": {
                "monthly": 7498941330,
                "daily": 0,
                "weekly": 7498941330
            },
            "username": "s-asadi",
            "package": {
                "monthly": 24.0,
                "daily": 3.0,
                "weekly": 9.0
            },
            "groupname": "PhD",
            "resetConfig": {
                "monthly": 1,
                "daily": "02:00 AM",
                "weekly": 5
            },
            "sessions": [
                {
                    "framedipaddress": "192.168.36.142",
                    "acctstarttime": "2017-02-26T00:43:54Z",
                    "usage": 4582063747,
                    "acctuniqueid": "903bb851e5f043ff99614df06687c1be",
                    "acctsessionid": "80200b78"
                },
                {
                    "framedipaddress": "192.168.36.142",
                    "acctstarttime": "2017-02-26T00:43:54Z",
                    "usage": 4582063747,
                    "acctuniqueid": "903bb851e5f043ff99614df06687c1be",
                    "acctsessionid": "80200b78"
                },
                {
                    "framedipaddress": "192.168.36.142",
                    "acctstarttime": "2017-02-26T00:43:54Z",
                    "usage": 4582063747,
                    "acctuniqueid": "903bb851e5f043ff99614df06687c1be",
                    "acctsessionid": "80200b78"
                }
            ]
        };

    const packages = [];
    for (let type of ['daily', 'weekly', 'monthly']) {

        const percent = response.usage[type] / (response.package[type] * 10000000);

        packages.push({
            usage: humanFileSize(response.usage[type]),
            total: humanFileSize(response.package[type] * 1000000000),
            percent,
            degree: Math.floor(percent / (100.0 / 180)),
            title: {daily: 'روزانه', weekly: 'هفتگی', monthly: 'ماهیانه'}[type],
            type,
            active: type === 'weekly',
        })
    }

    const sessions = response.sessions.map(s => {
        return {
            ip: s.framedipaddress,
            time: s.acctstarttime,
            usage: humanFileSize(s.usage),
            id: s.acctsessionid,
            username: s.username,
        }
    });

    return {
        packages,
        group: response.groupname,
        sessions,
    }
}

// http://stackoverflow.com/questions/10420352
function humanFileSize(bytes, si) {
    // var thresh = si ? 1000 : 1024;
    var thresh = 1000;
    if (Math.abs(bytes) < thresh) {
        return bytes + ' بایت';
    }
    var units = si
        ? ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        : ['کیلوبایت', 'مگابایت', 'گیگابایت', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
    var u = -1;
    do {
        bytes /= thresh;
        ++u;
    } while (Math.abs(bytes) >= thresh && u < units.length - 1);
    return bytes.toFixed(1) + ' ' + units[u];
}

module.exports = {
    user_usage
};