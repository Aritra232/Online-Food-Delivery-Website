document.addEventListener('DOMContentLoaded', () => {
    const cart = JSON.parse(localStorage.getItem('cart'));
    const orderItemsList = document.getElementById('orderItems');
    const totalPriceElement = document.getElementById('totalPrice');
    const totalPriceWithVATElement = document.getElementById('totalPriceWithVAT');
    const subtotalElement = document.getElementById('subtotal');
    const addressInput = document.getElementById('address');
    const cashPaymentRadio = document.getElementById('cashPayment');
    const onlinePaymentRadio = document.getElementById('onlinePayment');
    const confirmOrderBtn = document.getElementById('confirmOrderBtn');

    // Populate order summary
    if (cart && cart.length > 0) {
        let totalPrice = 0;
        cart.forEach(cartItem => {
            const orderItemElement = document.createElement('li');
            orderItemElement.textContent = `${cartItem.item.name} x ${cartItem.quantity} - $${cartItem.item.price * cartItem.quantity}`;
            orderItemsList.appendChild(orderItemElement);
            totalPrice += cartItem.item.price * cartItem.quantity;
        });

        // Calculate total price with VAT
        const VAT = totalPrice * 0.05;
        const totalPriceWithVAT = totalPrice + VAT;

        totalPriceElement.textContent = `Total Price: $${totalPrice.toFixed(2)}`;
        totalPriceWithVATElement.textContent = `Total Price with VAT (5%): $${totalPriceWithVAT.toFixed(2)}`;
        subtotalElement.textContent = `Subtotal: $${(totalPriceWithVAT + 60).toFixed(2)}`;
    } else {
        alert('No items found in the cart. Redirecting to the restaurant page.');
        window.location.href = '/html/restaurant.html'; // Redirect to restaurant page if cart is empty
    }

    // Event listener for confirm order button
    confirmOrderBtn.addEventListener('click', () => {
        const address = addressInput.value;
        const paymentMethod = cashPaymentRadio.checked ? 'Cash Payment' : 'Online Payment';
        if (!address) {
            alert('Please enter your address.');
        } else if (!cashPaymentRadio.checked && !onlinePaymentRadio.checked) {
            alert('Please select a payment method.');
        } else {
            if (paymentMethod === 'Cash Payment') {
                alert('Your order has been placed. Please wait for the delivery.');
            } else {
                // Handle online payment methods
                alert(`Your order has been placed. Please proceed with ${paymentMethod}.`);
            }
        }
    });
});
