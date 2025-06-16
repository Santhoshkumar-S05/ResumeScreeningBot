document.getElementById("resumeForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    const button = document.querySelector('button');
    const resultDiv = document.getElementById('result');
    const formData = new FormData(this);

    button.classList.add('loading');
    button.disabled = true;
    button.textContent = 'Analyzing...';

    try {
        const res = await fetch("/analyze_resume", {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        button.classList.remove('loading');
        button.disabled = false;
        button.textContent = '🔍 Analyze Resume';

        if (data.error) {
            resultDiv.innerHTML = `<div style="color:red;"><h2>⚠️ Analysis Error</h2><p>${data.error}</p></div>`;
            return;
        }

        let scoreColor = '#ef4444';
        if (data.score >= 80) scoreColor = '#10b981';
        else if (data.score >= 60) scoreColor = '#f59e0b';
        else if (data.score >= 40) scoreColor = '#f97316';

        resultDiv.innerHTML = `
            <div style="text-align:center;">
                <div style="font-size:2rem; color:${scoreColor}; font-weight:bold;">Score: ${data.score}/100</div>
                <p>${data.feedback}</p>
                <h3>🔍 Missing Keywords:</h3>
                <p>${data.missing.join(', ') || 'None'}</p>
            </div>
        `;
        resultDiv.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        button.classList.remove('loading');
        button.disabled = false;
        button.textContent = '🔍 Analyze Resume';
        resultDiv.innerHTML = `<div style="color:red;"><h2>⚠️ Error</h2><p>Something went wrong. Please try again.</p></div>`;
    }
});
