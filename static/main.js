// --- 1. TYPING EFFECT FOR HERO SECTION ---
document.addEventListener("DOMContentLoaded", function() {
    const roles = [
        "Full-Stack Python & Web Developer",
        "Android & Mobile App Builder",
        "Java ME Feature Phone Developer",
        "SQL Database Architect"
    ];
    let roleIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    const typedElement = document.getElementById("typed-role");

    function typeEffect() {
        if (!typedElement) return;
        const currentRole = roles[roleIndex];
        
        if (isDeleting) {
            typedElement.textContent = currentRole.substring(0, charIndex - 1);
            charIndex--;
        } else {
            typedElement.textContent = currentRole.substring(0, charIndex + 1);
            charIndex++;
        }

        let typeSpeed = isDeleting ? 50 : 100;

        if (!isDeleting && charIndex === currentRole.length) {
            typeSpeed = 2000; // Wait before deleting
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            roleIndex = (roleIndex + 1) % roles.length;
            typeSpeed = 500;
        }

        setTimeout(typeEffect, typeSpeed);
    }

    typeEffect();

    // --- 2. INTERACTIVE PROJECT FILTERING ---
    const filterButtons = document.querySelectorAll(".filter-btn");
    const projectCards = document.querySelectorAll(".project-card");

    filterButtons.forEach(button => {
        button.addEventListener("click", () => {
            // Active button styling toggle
            filterButtons.forEach(btn => btn.classList.remove("bg-indigo-600", "text-white"));
            filterButtons.forEach(btn => btn.classList.add("bg-gray-900", "text-gray-300"));
            button.classList.remove("bg-gray-900", "text-gray-300");
            button.classList.add("bg-indigo-600", "text-white");

            const filterValue = button.getAttribute("data-filter");

            projectCards.forEach(card => {
                const techStack = card.getAttribute("data-tech").toLowerCase();
                if (filterValue === "all" || techStack.includes(filterValue)) {
                    card.style.display = "flex";
                } else {
                    card.style.display = "none";
                }
            });
        });
    });
});