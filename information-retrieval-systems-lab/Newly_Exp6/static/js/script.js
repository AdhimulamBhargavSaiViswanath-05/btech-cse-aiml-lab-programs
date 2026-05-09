document.addEventListener('DOMContentLoaded', function() {
    const searchBtn = document.getElementById('searchBtn');
    const keywordInput = document.getElementById('keyword');
    const sourceSelect = document.getElementById('source');
    const statusDiv = document.getElementById('status');
    const resultsDiv = document.getElementById('results');
    const resultsContainer = document.getElementById('resultsContainer');
    const downloadBtn = document.getElementById('downloadBtn');
    
    let currentFilename = '';

    // Handle Enter key in keyword input
    keywordInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchBtn.click();
        }
    });

    searchBtn.addEventListener('click', async function() {
        const keyword = keywordInput.value.trim();
        const source = sourceSelect.value;

        if (!keyword) {
            showStatus('Please enter a search keyword', 'error');
            return;
        }

        // Disable button and show loader
        searchBtn.disabled = true;
        searchBtn.querySelector('.btn-text').textContent = 'Searching...';
        searchBtn.querySelector('.loader').style.display = 'inline-block';
        
        // Hide previous results
        resultsDiv.style.display = 'none';
        showStatus('Scraping news articles... This may take a moment.', 'info');

        try {
            const response = await fetch('/scrape', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ keyword, source })
            });

            const data = await response.json();

            if (data.success) {
                showStatus(`Found ${data.count} articles!`, 'success');
                currentResults = data.results; // Store results globally
                displayResults(data.results);
                currentFilename = data.filename;
                resultsDiv.style.display = 'block';
            } else {
                showStatus(data.message || 'No results found', 'error');
            }
        } catch (error) {
            showStatus('An error occurred: ' + error.message, 'error');
        } finally {
            // Re-enable button
            searchBtn.disabled = false;
            searchBtn.querySelector('.btn-text').textContent = 'Search News';
            searchBtn.querySelector('.loader').style.display = 'none';
        }
    });

    downloadBtn.addEventListener('click', function() {
        if (currentFilename) {
            window.location.href = `/download/${currentFilename}`;
        }
    });

    function showStatus(message, type) {
        statusDiv.textContent = message;
        statusDiv.className = `status-message ${type}`;
        statusDiv.style.display = 'block';
    }

    function displayResults(results) {
        resultsContainer.innerHTML = '';

        if (results.length === 0) {
            resultsContainer.innerHTML = `
                <div class="no-results">
                    <div class="no-results-icon">📭</div>
                    <p>No articles found</p>
                </div>
            `;
            return;
        }

        // Create table
        let tableHTML = `
            <table class="results-table">
                <thead>
                    <tr>
                        <th>Source</th>
                        <th>Headline</th>
                        <th>Date</th>
                        <th>Author</th>
                        <th>Snippet</th>
                        <th>Image</th>
                        <th>Link</th>
                        <th>Documentation</th>
                    </tr>
                </thead>
                <tbody>
        `;

        results.forEach((article, index) => {
            const imageHTML = article['Image URL'] && article['Image URL'] !== 'N/A' 
                ? `<img src="${article['Image URL']}" alt="Article" class="table-image" onerror="this.style.display='none'">`
                : 'N/A';
            
            tableHTML += `
                <tr>
                    <td class="table-source">${article.Source}</td>
                    <td class="table-headline">${article.Headline || 'Untitled'}</td>
                    <td class="table-date">${formatDate(article.Date)}</td>
                    <td>${article.Author || 'Unknown'}</td>
                    <td class="table-snippet">${article.Content_Snippet || 'No description available.'}</td>
                    <td class="table-image-cell">${imageHTML}</td>
                    <td>
                        <a href="${article.URL}" target="_blank" rel="noopener noreferrer">
                            View →
                        </a>
                    </td>
                    <td>
                        <button class="btn-doc" onclick="generateDoc(${index})">
                            Article Doc
                        </button>
                    </td>
                </tr>
            `;
        });

        tableHTML += `
                </tbody>
            </table>
        `;

        resultsContainer.innerHTML = tableHTML;
    }

    function formatDate(dateString) {
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', { 
                year: 'numeric', 
                month: 'short', 
                day: 'numeric' 
            });
        } catch {
            return dateString;
        }
    }
});

// Global variable to store current results
let currentResults = [];


// Function to open article documentation in new window
function generateDoc(articleIndex) {
    const article = currentResults[articleIndex]; // Make sure 'currentResults' has the data

    if (!article) {
        alert('Article data not found for index ' + articleIndex);
        return;
    }

    // Store article in sessionStorage (This is correct)
    sessionStorage.setItem('articleData', JSON.stringify(article));

    // --- CORRECTED LINE ---
    // Open the single documentation page URL in a new window/tab
    window.open('/article_doc', '_blank'); // REMOVE '+ articleIndex'
    // --- END CORRECTION ---
}