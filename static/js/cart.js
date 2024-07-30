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
    
    var cart = JSON.parse(getCookie('cart') || '{}'); // Initialize cart from cookie or as an empty object

    if (cart[productId] === undefined) {
        cart[productId] = { 'quantity': 1 };
    } else {
        if (action === 'add') {
            cart[productId]['quantity'] += 1;
        } else if (action === 'remove') {
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
            'X-CSRFToken': csrftoken, // Ensure CSRF token is sent
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
    .then(response => response.json())
    .then(data => {
        console.log('data:', data);
        location.reload();
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
