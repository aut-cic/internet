const Axios = require('axios');
const momentJ = require('moment-jalaali');
const {lookupIP} = require('../lib/ip');
const _ = require('lodash');

// process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

// Create axios instance
const _acct = Axios.create({
    baseURL: process.env.ACCT_URL || 'http://acct.aut.ac.ir:8001',
});

async function user_logout({username, ip}) {
    try {
        await _acct.get('api/v1/logout', {params: {username, ip}}).then(res => res.data);
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

async function user_usage({username, ip}) {
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
        let api_response = await _acct.get('api/v1/userusage', {params: {username, ip}}).then(res => res.data);

        if (typeof api_response === 'string') {
            return null;
        }
        response = _.defaultsDeep(api_response,response);
    } catch (e) {
        console.error('[usage]', username, ip);
        return null;
    }

    // Active type
    const active_type = get_active_type(response);


    // Packages
    const packages = [];

    for (let type of ['daily', 'weekly', 'monthly', 'free']) {
        let percent = response.usage[type] / (response.package[type] * Math.pow(1024, 3)) * 100;

        if (percent > 100) {
            percent = 100;
        }

        let color = 'success';
        if (percent > 66) {
            color = 'danger';
        } else if (percent > 33) {
            color = 'warning';
        }

        packages.push({
            usage: humanFileSize(response.usage[type]),
            total: humanFileSize(response.package[type] * Math.pow(1024, 3)),
            percent,
            degree: Math.floor(percent / (100.0 / 180)),
            title: {daily: 'روزانه', weekly: 'هفتگی', monthly: 'ماهیانه'}[type],
            title2: {
                daily: 'سرعت نامحدود',
                weekly: 'سرعت زیاد',
                monthly: (response.speeds.monthly||'').split('/')[1],
                free: 'سرعت آزاد'
            }[type],
            color,
            color2: {daily: 'success', weekly: 'primary', monthly: 'warning', free: 'danger'}[type],
            type,
            active: type === active_type,
        });
    }

    const sessions = response.sessions.map(s => {

        let location = lookupIP(s.framedipaddress);

        return {
            ip: s.framedipaddress,
            time: new momentJ(s.acctstarttime).format('HH:mm:ss - jYYYY/jM/jD'),
            usage: s.usage < 1000 ? '-' : humanFileSize(s.usage),
            id: s.acctsessionid,
            location: location ? location.description : '-',
        }
    });

    return {
        packages,
        group: (response.groupname || '').split('-')[0],
        sessions,
        username: response.username,
        active_type,
    }
}


// http://stackoverflow.com/questions/10420352
const units = ['کیلوبایت', 'مگابایت', 'گیگابایت', 'ترابایت', 'PiB', 'EiB', 'ZiB', 'YiB'];

function humanFileSize(bytes, si) {
    const thresh = 1024;

    if (Math.abs(bytes) < thresh) {
        // return bytes + ' بایت';
        return '-';
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