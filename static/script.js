document.addEventListener('DOMContentLoaded', () => {
    const factE1 = document.getElementById('fact');
    const btn =document.getElementById('getFact');
    const status = document.getElementById('status');
    const sourceHint = document.getElementById('sourceHint');

    async function fetchFact() {
        status.textContent = "Loading...";
        try {
            const response = await fetch("/api/random-fact");
            if (!response.ok) throw new Error("Network response was not OK.");
            const data = await response.json();
            if (data.error) {
                factE1.textContent = "Error: " + (data.error || "Unknown");
                status.textContent = data.detail || "";
                return;
            }
            let text = data.fact || JSON.stringify(data);
            if (sourceHint.checked && data.source) {
                text += `  - (${data.source})`;
            }
            factE1.textContent = text;
            status.textContent = "";
        } catch (err) {
            factE1.textContent = "Failed to fetch fact";
            status.textContent = err.message;
        }
    }

    btn.addEventListener("click", fetchFact);
});