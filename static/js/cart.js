let updateBtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        let productId = this.dataset.product
        let action = this.dataset.action

        if (user === 'AnonymousUser') {
            addCookieItem(productId, action)
        } else {
            updateUserOrder(productId, action)
        }
    })
}

function addCookieItem(productId, action) {
    if (action === 'add') {
        if (cart[productId] == null) {
            cart[productId] = {'quantity': 1}
        } else {
            cart[productId]['quantity'] += 1
        }
    }

    if (action === "remove") {
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0) {
            delete cart[productId]
        }
    }
}

function updateUserOrder(productId, action) {
    console.log("User is authenticated, send data")

    const url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action
        })
    }).then((response) => {
        return response.json()
    })
        .then((data) => {
            console.log(data)
        })
}

