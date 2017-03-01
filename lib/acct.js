const Axios = require('axios');
const momentJ = require('moment-jalaali');
const {lookupIP} = require('../lib/ip');

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

async function user_usage({username, ip}) {
    let response;

    try {
        response = await _acct.get('api/v1/userusage', {params: {username, ip}}).then(res => res.data);
        if (typeof response === 'string') {
            return null;
        }
    } catch (e) {
        console.error('[usage]', username, ip);
        return null;
    }

    const packages = [];

    let active_type = 'daily';

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
            title2: {daily: 'سرعت نامحدود', weekly: 'سرعت زیاد', monthly: 'سرعت معمولی'}[type],
            color,
            color2: {daily: 'success', weekly: 'warning', monthly: 'danger'}[type],
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
        group: response.groupname,
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
        return bytes + ' بایت';
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