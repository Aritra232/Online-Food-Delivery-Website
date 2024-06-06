// Sample items data
const items = [
    { name: "Item 1", price: 10 },
    { name: "Item 2", price: 15 },
    { name: "Item 3", price: 20 }
];

// Function to display order items
function displayOrderItems() {
    const orderSummary = document.getElementById("orderSummary");
    orderSummary.innerHTML = ""; // Clear previous items

    let totalPrice = 0;
    items.forEach(item => {
        const itemElement = document.createElement("div");
        itemElement.classList.add("item");
        itemElement.innerHTML = `
            <p>${item.name}</p>
            <p>${item.price}</p>
            <button class="quantityButton" data-index="${items.indexOf(item)}">-</button>
            <span>1</span>
            <button class="quantityButton" data-index="${items.indexOf(item)}">+</button>
        `;
        orderSummary.appendChild(itemElement);
        totalPrice += item.price;
    });

    // Calculate and display VAT
    const vatAmount = totalPrice * 0.05;
    document.getElementById("vatAmount").textContent = vatAmount;

    // Calculate and display total price including VAT and delivery charge
    const totalAmount = totalPrice + vatAmount + 60;
    document.getElementById("totalAmount").textContent = totalAmount.toFixed(2);

    // Add event listeners for quantity buttons
    const quantityButtons = document.querySelectorAll(".quantityButton");
    quantityButtons.forEach(button => {
        button.addEventListener("click", updateQuantity);
    });
}

// Function to update item quantity
function updateQuantity(event) {
    const index = parseInt(event.target.getAttribute("data-index"));
    const operation = event.target.textContent;
    const quantityElement = event.target.parentElement.querySelector("span");
    let quantity = parseInt(quantityElement.textContent);

    if (operation === "-") {
        quantity = Math.max(1, quantity - 1);
    } else if (operation === "+") {
        quantity++;
    }

    quantityElement.textContent = quantity;
}

// Display order items when the page loads
document.addEventListener("DOMContentLoaded", displayOrderItems);

// Checkout button functionality
document.getElementById("checkoutButton").addEventListener("click", function() {
    // Redirect to the checkout page or perform further checkout actions
    console.log("Redirecting to checkout page...");
});
