const MESSAGES = {
    INTERNET_LOGIN: {
        fa: 'ورود به اینترنت',
        en: 'Internet Login'
    },
    LOGIN: {
        fa: 'ورود',
        en: 'Login'
    },
    EMAIL: {
        fa: 'آدرس رایانامه',
        en: 'Email Address'
    },
    PASSWORD: {
        fa: 'رمز عبور',
        en: 'Password'
    },
    NO_ID: {
        fa: 'شناسه کاربری ندارم',
        en: 'I have not username'
    },
    GUEST_LOGIN: {
        fa: 'ورود بدون شناسه (سرعت پایین)',
        en: 'guest login (low speed)'
    },
    FORGOT_PASSWORD: {
        fa: 'رمز ورود خودم را فراموش کرده ام',
        en: 'forgot my password'
    },
    CHANGE_PASSWORD: {
        fa: 'تغییر کد واژه',
        en: 'change password'
    },
    OTHER_LANG: {
        fa: 'English',
        en: 'فارسی'
    },
    _OTHER_LANG_KEY: {
        fa: 'en',
        en: 'fa'
    }
};

const getMessages = (lang = 'fa') => {
    let msg = {};
    for (let key in MESSAGES) {
        msg[key] = MESSAGES[key][lang];
    }
    return msg;
};

module.exports = {
    fa: getMessages('fa'),
    en: getMessages('en')
};