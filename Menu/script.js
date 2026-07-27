const menuItems = [
    {
        section: "main",
        name: "Picada Colombiana",
        description: "Pork ribs, crispy pork belly, chicken, chorizo, corn on the cob, ripe plantains, and yellow and white potatoes.",
        price: "$26",
        image: "img/Picada.png",
        featured: true
    },
    {
        section: "main",
        name: "Frijolada",
        description: "Colombian beans served with rice, chorizo, ripe plantain, and avocado.",
        price: "$20",
        image: "img/Cazuela.png"
    },
    {
        section: "main",
        name: "Arroz Paisa",
        description: "Rice with chorizo, pork ribs, chicken, corn, ripe plantain, and bacon.",
        price: "$20",
        image: "img/ArrozPaisa.png"
    },
    {
        section: "main",
        name: "Arroz con Pollo",
        description: "Rice with shredded chicken, bell pepper, onion, carrot, peas, and corn.",
        price: "$20",
        image: "img/ArrozConPollo.png"
    },
    {
        section: "soups",
        name: "Ajiaco",
        description: "Colombian chicken soup with yellow and white potatoes, corn on the cob, scallions, cream, capers, avocado, and white rice.",
        price: "$20",
        image: "img/Ajiaco.png",
        seasonal: true
    },
    {
        section: "soups",
        name: "Sancocho",
        description: "Traditional soup with yellow and white potatoes, cassava, chicken, pork rib, and corn on the cob.",
        price: "$20",
        image: "img/Sancocho.png",
        seasonal: true
    },
    {
        section: "breakfast",
        name: "Huevos Pericos",
        description: "Colombian-style scrambled eggs with tomato and scallions.",
        price: "$10",
        image: "img/HuevosPericos.png"
    },
    {
        section: "breakfast",
        name: "Huevos Pericos con Arroz",
        description: "Colombian-style scrambled eggs with tomato and scallions, served with white rice.",
        price: "$13",
        image: "img/HuevosPericosConArroz.jpg"
    },
    {
        section: "breakfast",
        name: "Huevos Pericos con Arepa",
        description: "Colombian-style scrambled eggs with tomato and scallions, served with a corn arepa.",
        price: "$16",
        image: "img/HuevosPericosConArepa.jpg"
    },
    {
        section: "breakfast",
        name: "Caldo de Costilla",
        description: "Beef rib broth with potatoes, scallions, and cilantro.",
        price: "$16",
        image: "img/CaldoDeCostilla.png"
    },
    {
        section: "breakfast",
        name: "Caldo de Pollo",
        description: "Colombian chicken broth with a square-cut chicken piece, sliced potatoes, scallions, and cilantro.",
        price: "$16",
        image: "img/CaldoDePollo.jpg"
    },
    {
        section: "breakfast",
        name: "Chocolate Caliente",
        description: "Warm Colombian-style hot chocolate.",
        price: "$5",
        image: "img/HotChocolate.png"
    },
    {
        section: "breakfast",
        name: "2 Arepas con Queso",
        description: "Two grilled corn arepas served with cheese.",
        price: "$5",
        image: "img/Arepas.png"
    },
    {
        section: "breakfast",
        name: "Papa Rellena",
        description: "Crispy potato stuffed with seasoned ground beef and egg.",
        price: "$8",
        image: "img/PapaRellenaCarne.jpg"
    },
    {
        section: "breakfast",
        name: "Empanada",
        description: "Crispy corn pastry with a savory meat, rice, egg, and potato filling. Guava and cheese is also available.",
        price: "1 for $6 | 2 for $10",
        image: "img/Empanadas.png"
    },
    {
        section: "drinks",
        name: "Soda",
        description: "Chilled canned soda.",
        price: "$1",
        image: "img/Soda.jpg"
    },
    {
        section: "drinks",
        name: "Agua",
        description: "Chilled bottled water.",
        price: "$1",
        image: "img/Agua.jpg"
    },
    {
        section: "drinks",
        name: "Limonada Natural",
        description: "Fresh lime juice with cold water, natural sugar, and ice.",
        price: "12 oz $5",
        image: "img/Limonada.png"
    },
    {
        section: "drinks",
        name: "Limonada Cremosa",
        description: "Fresh lime juice blended with condensed milk and ice for a smooth, sweet, and refreshing drink.",
        price: "16 oz $8",
        image: "img/Cremosa.png"
    },
    {
        section: "drinks",
        name: "Jugo de Naranja Natural",
        description: "Freshly squeezed orange juice.",
        price: "12 oz $6",
        image: "img/Naranja.png"
    },
    {
        section: "drinks",
        name: "Salpicón",
        description: "Refreshing Colombian fruit mix with watermelon, papaya, pineapple, melon, and other fresh fruit in a sweet, juicy base.",
        price: "16 oz $9",
        image: "img/Salpicon.png"
    }
];

const popup = document.getElementById("item-popup");
const popupVisual = document.getElementById("popup-visual");
const popupDish = document.getElementById("popup-dish");
const popupDescription = document.getElementById("popup-description");
const popupPrice = document.getElementById("popup-price");
const popupSeasonal = document.getElementById("popup-seasonal");
const popupFeatured = document.getElementById("popup-featured");
let lastTrigger = null;

function visualMarkup(item) {
    if (item.image) {
        return `<img src="${item.image}" alt="" loading="lazy" decoding="async">`;
    }

    const tone = item.tone === "soda" ? " tone-soda" : "";
    return `<div class="menu-card-placeholder${tone}" aria-hidden="true"><span>${item.placeholder}</span></div>`;
}

function cardMarkup(item, index) {
    const seasonal = item.seasonal
        ? '<span class="card-seasonal">Unavailable during summer</span>'
        : "";
    const featured = item.featured
        ? '<span class="card-featured">House Special</span>'
        : "";
    const featuredClass = item.featured ? " is-featured" : "";

    return `
        <button class="menu-card${featuredClass}" type="button" data-menu-index="${index}" aria-haspopup="dialog" aria-controls="item-popup">
            ${visualMarkup(item)}
            <span class="menu-card-body">
                ${featured}
                <span class="card-title">${item.name}</span>
                <span class="card-price">${item.price}</span>
                ${seasonal}
                <span class="btn-view">View details</span>
            </span>
        </button>`;
}

document.querySelectorAll("[data-menu-section]").forEach((container) => {
    const section = container.dataset.menuSection;
    container.innerHTML = menuItems
        .map((item, index) => ({ item, index }))
        .filter(({ item }) => item.section === section)
        .map(({ item, index }) => cardMarkup(item, index))
        .join("");
});

function openPopup(index, trigger) {
    const item = menuItems[index];
    if (!item || !popup) {
        return;
    }

    lastTrigger = trigger;
    popupVisual.innerHTML = visualMarkup(item);
    popupDish.textContent = item.name;
    popupDescription.textContent = item.description;
    popupPrice.textContent = item.price;
    popupSeasonal.hidden = !item.seasonal;
    popupFeatured.hidden = !item.featured;
    popup.classList.add("is-open");
    popup.setAttribute("aria-hidden", "false");
    document.body.classList.add("popup-open");
    popup.querySelector(".popup-close").focus();
}

function closePopup() {
    if (!popup || !popup.classList.contains("is-open")) {
        return;
    }

    popup.classList.remove("is-open");
    popup.setAttribute("aria-hidden", "true");
    document.body.classList.remove("popup-open");

    if (lastTrigger) {
        lastTrigger.focus();
    }
}

document.addEventListener("click", (event) => {
    const card = event.target.closest("[data-menu-index]");
    if (card) {
        openPopup(Number(card.dataset.menuIndex), card);
        return;
    }

    if (event.target === popup || event.target.closest("[data-close-popup]")) {
        closePopup();
    }
});

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        closePopup();
        return;
    }

    if (event.key === "Tab" && popup.classList.contains("is-open")) {
        event.preventDefault();
        popup.querySelector(".popup-close").focus();
    }
});
