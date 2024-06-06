let map;

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 23.8103, lng: 90.4125 },
        zoom: 8,
    });

    const marker = new google.maps.Marker({
        position: { lat: 23.8103, lng: 90.4125 },
        map,
        draggable: true,
        animation: google.maps.Animation.DROP,
    });

    marker.addListener("dragend", () => {
        updateMarkerPosition(marker.getPosition());
    });
}

function updateMarkerPosition(position) {
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ location: position }, (results, status) => {
        if (status === "OK") {
            if (results[0]) {
                const address = results[0].formatted_address;
                document.getElementById("homeAddress").value = address;
            } else {
                console.log("No address found");
            }
        } else {
            console.log("Geocoder failed due to: " + status);
        }
    });
}

document.getElementById("signupForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const phoneNumber = document.getElementById("phoneNumber").value;
    const firstName = document.getElementById("firstName").value;
    const lastName = document.getElementById("lastName").value;
    const email = document.getElementById("email").value;
    const homeAddress = document.getElementById("homeAddress").value;

    console.log("Phone Number:", phoneNumber);
    console.log("First Name:", firstName);
    console.log("Last Name:", lastName);
    console.log("Email:", email);
    console.log("Home Address:", homeAddress);
});
