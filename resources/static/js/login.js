function fixLoginForm() {
    document.login.username.value = (document.login.username.value || '')
        .split('@')[0]
        .toLowerCase()
        .replace(/[^\x00-\x7F]/g, "");
}

function guestLogin() {
    document.login.username.value = "guest";
    document.login.password.value = "guest";
    document.getElementById("cookie").value = "true";
    document.login.submit();
}

(function (i, s, o, g, r, a, m) {
    i['GoogleAnalyticsObject'] = r;
    i[r] = i[r] || function () {
            (i[r].q = i[r].q || []).push(arguments)
        }, i[r].l = 1 * new Date();
    a = s.createElement(o),
        m = s.getElementsByTagName(o)[0];
    a.async = 1;
    a.src = g;
    m.parentNode.insertBefore(a, m)
})(window, document, 'script', 'https://www.google-analytics.com/analytics.js', 'ga');

ga('create', 'UA-92789659-1', 'auto');
ga('send', 'pageview');