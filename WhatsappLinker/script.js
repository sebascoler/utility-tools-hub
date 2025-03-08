async function generateLink() {
    const phone = document.getElementById('phone').value.replace(/[^0-9]/g, '');
    const message = encodeURIComponent(document.getElementById('message').value);
    
    const whatsappUrl = `https://wa.me/${phone}?text=${message}`;
    
    try {
        const response = await fetch(`https://tinyurl.com/api-create.php?url=${encodeURIComponent(whatsappUrl)}`);
        const shortUrl = await response.text();
        
        const resultDiv = document.getElementById('result');
        const linkElement = document.getElementById('whatsappLink');
        
        linkElement.href = shortUrl;
        linkElement.textContent = shortUrl;
        resultDiv.style.display = 'block';
    } catch (error) {
        alert('Error creating short URL. Using full URL instead.');
        const resultDiv = document.getElementById('result');
        const linkElement = document.getElementById('whatsappLink');
        
        linkElement.href = whatsappUrl;
        linkElement.textContent = whatsappUrl;
        resultDiv.style.display = 'block';
    }
}

document.getElementById('generateBtn').addEventListener('click', generateLink); 