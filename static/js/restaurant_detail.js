document.addEventListener('DOMContentLoaded', function() {
    const increaseButtons = document.querySelectorAll('.increase-quantity');
    const decreaseButtons = document.querySelectorAll('.decrease-quantity');
    const quantityInputs = document.querySelectorAll('.quantity');

    increaseButtons.forEach((button, index) => {
        button.addEventListener('click', () => {
            quantityInputs[index].value++;
        });
    });

    decreaseButtons.forEach((button, index) => {
        button.addEventListener('click', () => {
            if (quantityInputs[index].value > 0) {
                quantityInputs[index].value--;
            }
        });
    });
});
