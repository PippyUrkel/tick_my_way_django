const bannerButtons = document.querySelectorAll('.banner-img button');
const badgeButtons = document.querySelectorAll('.badge-img button');
const bannerPurchaseButton = document.querySelector('.banner-buy-button');
const badgePurchaseButton = document.querySelector('.badge-buy-button');

let selectedBanner = null;
let selectedBadge = null;

function resetBorders(buttons) {
    buttons.forEach(button => {
        button.style.border = 'none'; 
    });
}

bannerButtons.forEach((button, index) => {
    button.addEventListener('click', () => {
        resetBorders(bannerButtons);
        button.style.border = '2px solid #000000'; 

        selectedBanner = `Banner ${index + 1}`;
        alert(`You selected ${selectedBanner}`);
    });
});

badgeButtons.forEach((button, index) => {
    button.addEventListener('click', () => {
        resetBorders(badgeButtons);
        button.style.border = '2px solid #000000';

        selectedBadge = `Badge ${index + 1}`;
        alert(`You selected ${selectedBadge}`);
    });
});

bannerPurchaseButton.addEventListener('click', () => {
    if (selectedBanner) {
        alert(`${selectedBanner} purchased successfully!`);
    } else {
        alert('Please select a banner before purchasing.');
    }
});

badgePurchaseButton.addEventListener('click', () => {
    if (selectedBadge) {
        alert(`${selectedBadge} purchased successfully!`);
    } else {
        alert('Please select a badge before purchasing.');
    }
});
