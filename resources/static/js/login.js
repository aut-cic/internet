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


(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
        (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-92789659-1', 'auto');
ga('send', 'pageview');