const Axios = require('axios');
const momentJ = require('moment-jalaali');
const _ = require('lodash');
const {lookupIP} = require('../lib/ip');
const {get, set, drop} = require('../lib/cache');

// process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

// Create axios instance
const _acct = Axios.create({
    baseURL: process.env.ACCT_URL || 'http://192.168.2.233:8001',
});

async function user_logout({username, ip, acctuniqueid}) {
    try {
        await _acct.get('api/v1/logout', {params: {username, ip, acctuniqueid}}).then(res => res.data);

        // Invalidate cache
        // const cache_key = username || ip;
        // await drop(cache_key);

        return true;
    } catch (e) {
        console.error('[logout]', username, ip);
        return false;
    }
}

function get_active_type(response) {
    switch ((response.groupname || '').split('-')[1]) {
        case 'H1':
            return 'weekly';
        case 'H2':
            return 'monthly';
        case 'H3':
            return 'free';
        default:
            return 'daily';
    }
}

async function user_usage({username, ip}, use_cache = true) {
    let response = {
        resetConfig: {daily: 0, monthly: 0, weekly: 0},
        speeds: {
            monthly: '1M/2M'
        },
        groupname: '',
        package: {daily: 0, monthly: 0, weekly: 0, free: 0},
        usage: {daily: 0, monthly: 0, weekly: 0},
        sessions: [],
        username: ''
    };

    try {
        const cache_key = username || ip;
        let api_response;

        // if (use_cache) {
        //     api_response = await get(cache_key);
        // }

        if (!api_response) {
            api_response = await _acct.get('api/v1/userusage', {
                params: {
                    username: process.env.USERNAME || username,
                    ip: process.env.IP || ip
                },
                timeout: 1000
            }).then(res => res.data);

            // if (use_cache) {
            //     set(cache_key, response, 60)
            // }
        }

        if (typeof api_response === 'string') {
            return null;
        }

        response = _.defaultsDeep(api_response, response);

    } catch (e) {
        console.error('[usage]', e, username, ip);
        return null;
    }

    // Active type
    const active_type = get_active_type(response);

    // Packages
    const packages = [];

    // Free package
    response.package.free = 4 * response.package.monthly;
    response.usage.free = response.usage.monthly;

    for (let type of ['daily', 'weekly', 'monthly', 'free']) {
        let percent = response.usage[type] / (response.package[type] * Math.pow(1024, 3)) * 100;

        let color = 'success';
        if (percent > 66) {
            color = 'danger';
        } else if (percent > 33) {
            color = 'warning';
        }

        if (percent > 100 || isNaN(percent)) {
            percent = 100;
        }

        packages.push({
            usage: humanFileSize(response.usage[type]),
            total: humanFileSize(response.package[type] * Math.pow(1024, 3)),
            percent,
            degree: Math.floor(percent / (100.0 / 180)),
            title: {
                daily: 'روزانه',
                weekly: 'هفتگی',
                monthly: 'ماهیانه',
                free: 'آزاد'
            }[type],
            title2: {
                daily: 'سرعت نامحدود',
                weekly: 'سرعت زیاد',
                monthly: 'سرعت ' + (response.speeds.monthly || '').split('/')[1],
                free: 'سرعت کم'
            }[type],
            color,
            color2: {daily: 'success', weekly: 'primary', monthly: 'info', free: 'warning'}[type],
            type,
            active: type === active_type,
        });
    }

    let current_session = null;

    const sessions = response.sessions.map(s => {

        let location = lookupIP(s.framedipaddress);
        let is_current = s.framedipaddress === ip;

        let session = {
            ip: s.framedipaddress,
            time: new momentJ(s.acctstarttime).format('HH:mm:ss - jYYYY/jM/jD'),
            usage: s.usage < 1000 ? '-' : humanFileSize(s.usage),
            id: s.acctuniqueid,
            location: location ? location.description : '-',
            is_current,
        };

        if (is_current) {
            current_session = session;
        }

        return session;
    });

    if (!current_session) {
        return null;
    }

    return {
        packages,
        group: (response.groupname || '').split('-')[0],
        sessions,
        username: response.username,
        active_type,
        current_session,
    }
}


// http://stackoverflow.com/questions/10420352
const units = ['کیلوبایت', 'مگابایت', 'گیگابایت', 'ترابایت', 'PiB', 'EiB', 'ZiB', 'YiB'];

function humanFileSize(bytes, si) {
    const thresh = 1024;

    if (isNaN(bytes)) {
        return '∞';
    }

    if (Math.abs(bytes) < thresh) {
        // return bytes + ' بایت';
        // return '-';
        return '0 مگابایت';
    }

    let u = -1;

    do {
        bytes /= thresh;
        ++u;
    } while (Math.abs(bytes) >= thresh && u < units.length - 1);

    if (u < 2 || ((bytes * 10) % 10) === 0)
        return bytes.toFixed(0) + ' ' + units[u];

    return bytes.toFixed(1) + ' ' + units[u];
}

module.exports = {
    user_usage,
    user_logout
};