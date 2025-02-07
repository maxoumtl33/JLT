function scrollHeader() {
    const header = document.querySelector(".header"); // Assure-toi que c'est bien la bonne classe/ID

    if (!header) {
        console.error("L'élément '.header' est introuvable.");
        return;
    }

    window.addEventListener("scroll", () => {
        if (window.scrollY > 50) {
            header.classList.add("scrolled");
        } else {
            header.classList.remove("scrolled");
        }
    });
}

document.addEventListener("DOMContentLoaded", scrollHeader);
