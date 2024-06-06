document.addEventListener('DOMContentLoaded', function() {
    const restaurantDivs = document.querySelectorAll('.restaurant');
    restaurantDivs.forEach(restaurantDiv => {
        restaurantDiv.addEventListener('click', function() {
            const restaurantId = this.getAttribute('data-id');
            window.location.href = `/restaurant/${restaurantId}/`;
        });
    });
});
