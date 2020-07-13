let user = '{{ request.user }}';

function getCookieToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[1].trim()
            // Cookie string begin with name we want?

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue
}

let csrftoken = getCookieToken('csrftoken');


function getCookie(name) {
    const cookieArr = document.cookie.split(';')
    for (let i = 0; i < cookieArr.length; i++) {
        const cookiePair = cookieArr[i].split("=")
        if (name === cookiePair[0].trim()) {
            return decodeURIComponent(cookiePair[1])
        }
    }
    return null
}

let cart = JSON.parse(getCookie('cart'))
if (cart == null) {
    cart = {}
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"
}