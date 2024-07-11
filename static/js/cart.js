var updateBtns = document.getElementsByClassName('update-cart');

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'action:', action);

        if (user === 'AnonymousUser') {
            addCookieItem(productId, action);
        } else {
            updateUserOrder(productId, action);
        }
    });
}

function addCookieItem(productId, action) {
    console.log('Not logged in...');

    if (cart[productId] == undefined) {
        cart[productId] = { 'quantity': 1 };
    } else {
        if (action == 'add') {
            cart[productId]['quantity'] += 1;
        } else if (action == 'remove') {
            cart[productId]['quantity'] -= 1;
            if (cart[productId]['quantity'] <= 0) {
                delete cart[productId];
            }
        }
    }
    console.log('cart:', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    location.reload();
}

function updateUserOrder(productId, action) {
    console.log('User is logged in, sending data...');

    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
    .then(response => response.json())
    .then(data => {
        console.log('data:', data);
        location.reload();
    });
}
