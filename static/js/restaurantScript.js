document.addEventListener('DOMContentLoaded', () => {
    const selectedRestaurant = JSON.parse(localStorage.getItem('selectedRestaurant'));
    const restaurantName = document.getElementById('restaurantName');
    const itemList = document.getElementById('itemList');
    const cartItems = document.getElementById('cartItems');
    const checkoutBtn = document.getElementById('checkoutBtn');
    let cart = [];

    if (selectedRestaurant) {
        restaurantName.textContent = selectedRestaurant.name;
        selectedRestaurant.items.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.classList.add('item');
            itemElement.innerHTML = `
                <img src="${item.picture}" alt="${item.name}">
    <p>${item.name}</p>
    <p>$${item.price}</p>
    <select class="item-select">
        <option value="0">Select Quantity</option>
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4</option>
        <option value="5">5</option>
<option value="6">6</option>
<option value="7">7</option>
<option value="8">8</option>
<option value="9">9</option>
<option value="10">10</option>


                </select>
            `;
            itemList.appendChild(itemElement);

            const select = itemElement.querySelector('.item-select');
            select.addEventListener('change', () => {
                const quantity = parseInt(select.value);
                if (quantity > 0) {
                    addToCart(item, quantity);
                }
            });
        });
    } else {
        restaurantName.textContent = 'No restaurant selected';
    }

    function addToCart(item, quantity) {
        const existingItemIndex = cart.findIndex(cartItem => cartItem.item.name === item.name);
        if (existingItemIndex !== -1) {
            cart[existingItemIndex].quantity += quantity;
        } else {
            cart.push({ item: item, quantity: quantity });
        }
        renderCart();
    }

    function renderCart() {
        cartItems.innerHTML = '';
        cart.forEach(cartItem => {
            const cartItemElement = document.createElement('li');
            cartItemElement.textContent = `${cartItem.item.name} x ${cartItem.quantity} - $${cartItem.item.price * cartItem.quantity}`;
            cartItems.appendChild(cartItemElement);
        });
    }

    checkoutBtn.addEventListener('click', () => {
        // Implement checkout functionality here
        alert('Checkout functionality will be implemented in the future.');
    });
});
// JavaScript for item selection page
// Add event listener for checkout button
document.getElementById('checkoutBtn').addEventListener('click', () => {
    // Redirect to checkout page
    window.location.href = 'order_summary.html';
});

// Load restaurant details from localStorage
const selectedRestaurant = JSON.parse(localStorage.getItem('selectedRestaurant'));
if (selectedRestaurant) {
    document.getElementById('restaurantName').textContent = selectedRestaurant.name;
    const itemList = document.getElementById('itemList');
    selectedRestaurant.items.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.classList.add('item');
        itemElement.textContent = `${item.name} - $${item.price}`;
        itemList.appendChild(itemElement);
    });
}
function redirectToCheckout() {
    localStorage.setItem('cart', JSON.stringify(cart));
    window.location.href = 'order_summary.html';
}

// Event listener for checkout button
checkoutBtn.addEventListener('click', redirectToCheckout);