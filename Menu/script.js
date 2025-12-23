function openPopup(id) {
    document.getElementById(`popup-${id}`).style.display = "flex";
}

window.onclick = function(event) {
    if (event.target.classList.contains("popup")) {
    event.target.style.display = "none";
    }
};

function closePopup(){
    document.querySelectorAll('.popup').forEach(p => p.style.display = "none");
}
