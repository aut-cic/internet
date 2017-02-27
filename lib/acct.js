const Axios = require('axios');

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

// Create axios instance
const _acct = Axios.create({
    baseURL: process.env.ACCT_URL || 'http://acct.aut.ac.ir:8001',
});

async function user_usage({username, ip}) {
    let response;

    try {
        response = await _acct.get('api/v1/userusage', {params: {username, ip}}).then(res => res.data);
        if (typeof response === 'string') {
            throw response;
        }
    } catch (e) {
        throw e;
    }

    response = response || {
            "speeds": {
                "PhD-H1": "",
                "PhD": "",
                "PhD-H2": "",
                "PhD-H3": ""
            },
            "usage": {
                "monthly": 0,
                "daily": 0,
                "weekly": 0
            },
            "username": "",
            "package": {
                "monthly": 0,
                "daily": 0,
                "weekly": 0
            },
            "groupname": "",
            "resetConfig": {
                "monthly": 0,
                "daily": "",
                "weekly": 0
            },
            "sessions": []
        };

    const packages = [];

    let active_type = null;

    switch ((response.groupname || '').split('-')[1]) {
        case 'H1':
            active_type = 'weekly';
            break;
        case 'H2':
            active_type = 'monthly';
            break;
        case 'H3':
            active_type = 'yearly';
            break;
        default:
            active_type = 'daily';
            break;
    }


    for (let type of ['daily', 'weekly', 'monthly']) {
        let percent = response.usage[type] / (response.package[type] * 10000000);
        if (percent > 100) {
            percent = 100;
        }

        packages.push({
            usage: humanFileSize(response.usage[type]),
            total: humanFileSize(response.package[type] * 1000000000),
            percent,
            degree: Math.floor(percent / (100.0 / 180)),
            title: {daily: 'روزانه', weekly: 'هفتگی', monthly: 'ماهیانه'}[type],
            type,
            active: type === active_type,
        });
    }

    const sessions = response.sessions.map(s => {
        return {
            ip: s.framedipaddress,
            time: s.acctstarttime,
            usage: humanFileSize(s.usage),
            id: s.acctsessionid,
            location: 'خوابگاه'
        }
    });

    return {
        packages,
        group: response.groupname,
        sessions,
        username: response.username,
        active_type,
    }
}


// http://stackoverflow.com/questions/10420352
function humanFileSize(bytes, si) {
    var thresh = si ? 1000 : 1024;

    if (Math.abs(bytes) < thresh) {
        return bytes + ' بایت';
    }
    var units = si
        ? ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        : ['کیلوبایت', 'مگابایت', 'گیگابایت', 'ترابایت', 'PiB', 'EiB', 'ZiB', 'YiB'];
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