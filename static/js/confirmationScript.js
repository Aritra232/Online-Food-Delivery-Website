document.addEventListener('DOMContentLoaded', () => {
    const cartItems = JSON.parse(localStorage.getItem('cart'));
    if (cartItems && cartItems.length > 0) {
        const orderSummaryElement = document.getElementById('orderSummary');
        const paymentMethod = 'Credit Card'; // Example payment method
        let subtotal = 0;
        cartItems.forEach(item => {
            subtotal += item.price * item.quantity;
            orderSummaryElement.innerHTML += `<p>${item.name} x ${item.quantity} - $${(item.price * item.quantity).toFixed(2)}</p>`;
        });
        const vat = subtotal * 0.05;
        const total = subtotal + vat + 60; // Delivery fee $60
        orderSummaryElement.innerHTML += `
            <p>Subtotal: $${subtotal.toFixed(2)}</p>
            <p>VAT (5%): $${vat.toFixed(2)}</p>
            <p>Delivery Fee: $60.00</p>
            <p><strong>Total: $${total.toFixed(2)}</strong></p>
        `;
        document.getElementById('paymentMethod').textContent = paymentMethod;
    }
});