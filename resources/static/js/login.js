function fix() {
    var user = document.login.username.value;
    var indx = user.indexOf("@aut.ac.ir");
    if (indx > 0)
        document.login.username.value = user.substring(0, indx);
    if (user === "test") {
        var username = $(document.login.username);
        var parent = $(username).closest('.input-group');
        parent.addClass('has-error has-feedback');
        if (typeof username.data("shown") === "undefined" || username.data("shown") === false) {
            username.popover('show');
        }

        return false;
    }
}

function guestLogin() {
    document.login.username.value = "test";
    document.login.password.value = "test";
    document.getElementById("cookie").value = "true";
    document.login.submit();
}

function getQueryParams(qs) {
    qs = qs.split('+').join(' ');
    var params = {},
        tokens,
        re = /[?&]?([^=]+)=([^&]*)/g;
    while (tokens = re.exec(qs)) {
        params[decodeURIComponent(tokens[1])] = decodeURIComponent(tokens[2]);
    }
    return params;
}

