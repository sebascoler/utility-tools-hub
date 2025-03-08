async function generateQR() {
    const input = document.getElementById('qr-input').value;
    if (!input) {
        alert('Please enter some text or URL');
        return;
    }

    try {
        const response = await fetch('/generate-qr', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data: input }),
        });
        const data = await response.json();
        
        const resultDiv = document.getElementById('qr-result');
        resultDiv.innerHTML = `<img src="${data.qr_code}" alt="QR Code" class="mx-auto">`;
    } catch (error) {
        console.error('Error:', error);
        alert('Error generating QR code');
    }
}

async function generateWhatsAppLink() {
    const phone = document.getElementById('phone-input').value;
    const message = document.getElementById('message-input').value;

    if (!phone) {
        alert('Please enter a phone number');
        return;
    }

    try {
        const response = await fetch('/generate-whatsapp-link', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ phone, message }),
        });
        const data = await response.json();
        
        const resultDiv = document.getElementById('whatsapp-result');
        resultDiv.innerHTML = `
            <a href="${data.link}" target="_blank" class="text-green-600 hover:underline break-all">
                ${data.link}
            </a>`;
    } catch (error) {
        console.error('Error:', error);
        alert('Error generating WhatsApp link');
    }
}

async function removeBackground() {
    const input = document.getElementById('image-input');
    if (!input.files || !input.files[0]) {
        alert('Please select an image');
        return;
    }

    const resultDiv = document.getElementById('image-result');
    resultDiv.innerHTML = '<p class="text-gray-600">Processing... Please wait.</p>';

    const formData = new FormData();
    formData.append('image', input.files[0]);

    try {
        const response = await fetch('/remove-background', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Server error');
        }

        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        resultDiv.innerHTML = `
            <div class="space-y-4">
                <img src="${data.processed_image}" alt="Processed Image" class="max-w-full mx-auto rounded-lg shadow-lg">
                <a href="${data.processed_image}" download="processed_image.png" 
                   class="inline-block bg-purple-600 text-white py-2 px-4 rounded-lg hover:bg-purple-700 transition-colors">
                    Download Image
                </a>
            </div>`;
    } catch (error) {
        console.error('Error:', error);
        resultDiv.innerHTML = `<p class="text-red-600">Error processing image: ${error.message}</p>`;
    }
}
