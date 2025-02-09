function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    window.scrollTo({
        top: element.offsetTop,
        behavior: "smooth"
    });
}


/* New JavaScript for Contact Page */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contact-form');
    const submitButton = form.querySelector('button.submit-btn');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        const name = form.querySelector('[name="name"]').value;
        const email = form.querySelector('[name="email"]').value;
        const message = form.querySelector('[name="message"]').value;

        // Simple validation
        if (!name || !email || !message) {
            alert("Please fill out all fields.");
            return;
        }

    
        alert("Thank you for your message! We will get back to you soon.");
        form.reset();
    });
});
