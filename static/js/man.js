let map;
let marker;

function initMap() {
    const mapOptions = {
        center: { lat: 40.7128, lng: -74.006 }, // Default center (New York)
        zoom: 12
    };
    map = new google.maps.Map(document.getElementById('map'), mapOptions);
}

document.addEventListener('DOMContentLoaded', function() {
    const acceptOrderBtn = document.getElementById('accept-order-btn');
    const rejectOrderBtn = document.getElementById('reject-order-btn');

    acceptOrderBtn.addEventListener('click', function() {
        // Code to accept the order
        console.log('Order accepted');
        // Simulate updating UI
        acceptOrderBtn.disabled = true;
        rejectOrderBtn.disabled = true;
    });

    rejectOrderBtn.addEventListener('click', function() {
        // Code to reject the order
        console.log('Order rejected');
        // Simulate updating UI
        acceptOrderBtn.disabled = true;
        rejectOrderBtn.disabled = true;
    });

    // Simulated data for order details
    const orderIdElement = document.getElementById('order-id');
    const customerNameElement = document.getElementById('customer-name');
    const deliveryAddressElement = document.getElementById('delivery-address');

    orderIdElement.textContent = '123456';
    customerNameElement.textContent = 'John Doe';
    deliveryAddressElement.textContent = '123 Main St';

    // Start real-time GPS tracking
    updateDriverLocation();
});

function updateDriverLocation() {
    // Simulate updating driver's location on map
    const randomLat = Math.random() * 0.02 - 0.01; // Random latitude change
    const randomLng = Math.random() * 0.02 - 0.01; // Random longitude change

    const newPosition = {
        lat: map.getCenter().lat() + randomLat,
        lng: map.getCenter().lng() + randomLng
    };

    // Create a new marker if it doesn't exist
    if (!marker) {
        marker = new google.maps.Marker({
            position: newPosition,
            map: map,
            title: 'Driver Location'
        });
    } else {
        // Update marker position
        marker.setPosition(newPosition);
    }

    // Center map to the new position
    map.setCenter(newPosition);

    // Continue tracking
    setTimeout(updateDriverLocation, 5000); // Update every 5 seconds
}
