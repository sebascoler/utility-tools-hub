// Form handling
document.getElementById('contact-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get form values
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        message: document.getElementById('message').value
    };

    // Here you would typically send the form data to a server
    console.log('Form submitted:', formData);
    
    // Show success message in Spanish
    alert('¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.');
    
    // Reset form
    this.reset();
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        
        window.scrollTo({
            top: target.offsetTop - 80, // Adjust for fixed header
            behavior: 'smooth'
        });
    });
});

// Animate property cards on scroll
const observerOptions = {
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.property-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'all 0.5s ease-out';
    observer.observe(card);
});

function generateQR() {
    const urlInput = document.getElementById('urlInput');
    const qrcodeDiv = document.getElementById('qrcode');
    const errorDiv = document.getElementById('error');
    
    // Clear previous QR code and error message
    qrcodeDiv.innerHTML = '';
    errorDiv.innerHTML = '';

    // Get the URL from input
    const url = urlInput.value.trim();

    // Validate URL
    try {
        new URL(url);
    } catch (e) {
        errorDiv.innerHTML = 'Please enter a valid URL (include http:// or https://)';
        return;
    }

    // Generate QR code
    new QRCode(qrcodeDiv, {
        text: url,
        width: 200,
        height: 200,
        colorDark: "#000000",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.H
    });
}

// Add event listener for Enter key
document.getElementById('urlInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        generateQR();
    }
}); 