function setCookie(cname, cvalue, exdays = 2) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function alreadyJoined() {
    return getCookie('joined') === 'true';
}

function joinModalCount() {
    return parseInt(getCookie('joinModal')) || 0
}

function sendEvent(action) {
    if (!window.ga) {
        return
    }

    ga('send', {
        hitType: 'event',
        eventCategory: 'modals',
        eventAction: action,
        eventLabel: 'Join Modal'
    });
}

function joinChannel() {
    setCookie('joined', 'true')
    sendEvent('joined')
    window.location = "tg://join?invite=AAAAAELOIjyeP5FUrzUs5A"
}

$(document).ready(function() {
    if (alreadyJoined() || joinModalCount() >= 3) {
        sendEvent('release')
        return
    }

    var modal = $('#joinModal').modal('show');

    modal.on('shown.bs.modal', function () {
        setCookie('joinModal', joinModalCount() + 1)
    })

    modal.on('hidden.bs.modal', function () {
        sendEvent('hidden')
    })
})