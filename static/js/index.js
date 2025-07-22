function loadQuote() {
    fetch('/api/random-quote')
    .then(res => res.json())
    .then(data => {
        document.getElementById('quote-text').innerText = `"${data.quote}"`;
        document.getElementById('quote-author').innerText = `— ${data.author}`;
        // document.getElementById('quote-categories').innerText = 
        // data.categories.length ? `Categories: ${data.categories.join(', ')}` : '';
    });
}

function classifyUserText() {
    const text = document.getElementById("user-input").value;
    const resultBox = document.getElementById("classified-result");

    // if (!text.trim()) {
    //     alert("Please enter something.");
    //     return;
    // }

    // Show loading message
    resultBox.innerHTML = 'Analyzing your thoughts...';

    fetch('/api/classify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            document.getElementById("classified-result").innerText = data.error;
        } else {
            document.getElementById("classified-result").innerHTML = `
            <p id="quote-text" class="serif">"${data.quote}"</p>
            <p id="quote-author">— ${data.author}</p>
            `;
        }
    })
    .catch(err => {
        console.error("Classification error:", err);
        document.getElementById("classified-result").innerText = "Error occurred.";
    });
}

loadQuote();