function openPopup(id) {
    const popup = document.getElementById(`popup-${id}`);

    if (!popup) {
        return;
    }

    popup.classList.add("is-open");
    popup.setAttribute("aria-hidden", "false");
    document.body.classList.add("popup-open");

    const closeButton = popup.querySelector(".popup-close");
    if (closeButton) {
        closeButton.focus();
    }
}

function closePopup(){
    document.querySelectorAll(".popup").forEach((popup) => {
        popup.classList.remove("is-open");
        popup.setAttribute("aria-hidden", "true");
    });

    document.body.classList.remove("popup-open");
}

document.querySelectorAll("[data-popup]").forEach((card) => {
    card.addEventListener("click", () => openPopup(card.dataset.popup));

    card.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            openPopup(card.dataset.popup);
        }
    });
});

document.addEventListener("click", (event) => {
    if (event.target.classList.contains("popup") || event.target.closest("[data-close-popup]")) {
        closePopup();
    }
});

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        closePopup();
    }
});
