document.addEventListener('DOMContentLoaded', () => {
    // Initialize the map
    const map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 23.8103, lng: 90.4125 }, // Default center (Dhaka)
        zoom: 12, // Default zoom level
    });

    // Add a marker when user clicks on the map
    const marker = new google.maps.Marker({
        map,
        draggable: true, // Allow the marker to be dragged
    });

    // Add an event listener to update the marker position when it is dragged
    marker.addListener('dragend', () => {
        updateMarkerPosition(marker.getPosition());
    });

    // Function to update the marker position and display the address
    function updateMarkerPosition(latLng) {
        marker.setPosition(latLng);
        // Reverse geocode the latLng to get the address
        const geocoder = new google.maps.Geocoder();
        geocoder.geocode({ location: latLng }, (results, status) => {
            if (status === 'OK') {
                if (results[0]) {
                    const address = results[0].formatted_address;
                    console.log(address); // Display the address (you can customize how to display it)
                    // You can also update a hidden input field with the address for form submission
                } else {
                    console.error('No results found');
                }
            } else {
                console.error(`Geocoder failed due to: ${status}`);
            }
        });
    }

    // Center the map on user's current location if available
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude,
            };
            map.setCenter(userLocation);
            marker.setPosition(userLocation);
            updateMarkerPosition(userLocation);
        }, () => {
            console.error('Error: The Geolocation service failed.');
        });
    } else {
        console.error('Error: Your browser doesn\'t support geolocation.');
    }
});
