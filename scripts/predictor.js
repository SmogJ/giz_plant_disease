const resultCont = document.querySelector('.resultContainer');
        const resultDiv = document.getElementById('result');
        
// File input onchange function
function previewImage(event) {
    // resultCont.style.display = 'block';
    resultDiv.style.display = 'none';
    const image = document.getElementById('uploadedImage');
    image.src = URL.createObjectURL(event.target.files[0]);
}

// Handle prediction results from the server
document.querySelector('form').onsubmit = async function(event) {
    event.preventDefault(); // Prevent form from submitting normally
    
    const formData = new FormData(event.target);
    const response = await fetch('/predict', {
        method: 'POST',
        body: formData,
    });
    const result = await response.json();
    
    // Display prediction result
    const disease = document.getElementById('disease');
    const confidence = document.getElementById('confidence');
    if (response.ok) {
        // resultCont.style.display = 'block';
        resultDiv.style.display = 'block';
        disease.innerHTML = `${result.predicted_disease} `;
        confidence.innerHTML = `(Confidence: ${result.confidence.toFixed(2)}%)`;
    } else {
        // resultCont.style.display = 'block';
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `Error: ${result.error}`;
    }
};