function loadQuote() {
    fetch('/api/random-quote')
    .then(res => res.json())
    .then(data => {
        document.getElementById('quote-text').innerText = `"${data.quote}"`;
        document.getElementById('quote-author').innerText = `— ${data.author}`;
        document.getElementById('quote-categories').innerText = 
        data.categories.length ? `Categories: ${data.categories.join(', ')}` : '';
    });
}

loadQuote();