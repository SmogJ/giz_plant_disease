function previewImage(event){
    const image = document.getElementById('uploadImage');
    image.src = URL.createObjectURL(event.target.file[0]);
    image.style.display = "block";
}


// Handle Prediction from the server
document.querySelector('form').onsubmit = async function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const response = await fetch("/predict", {
        method: "POST",
        body: formData,
    });

    //Render the file to Json

    const result = await response.json();

    // Display Prediction result

    const resultDiv= document.getElementById("result");

    //If there is a response
    if (response.ok){
        resultDiv.innerHTML = `predicted Disease: ${result.presicted_disease} (Confidence: ${result.confidence.toFixed(2)}%)`;
    
    //If there is no reponse
    }else{
        resultDiv.innerHTML = `Error: ${result.error}`;
    };
}