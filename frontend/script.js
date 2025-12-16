const askBtn = document.getElementById("askBtn");
const input = document.getElementById("questionInput");
const conversation = document.getElementById("conversation");

askBtn.onclick = async () => {
    const question = input.value.trim();
    if (!question) return;

    conversation.innerHTML = `
        <p><strong>You:</strong> ${question}</p>
        <p><strong>ALVIN:</strong> Loading...</p>
    `;

    try {
        const res = await fetch("http://127.0.0.1:8000/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });

        const data = await res.json();

        conversation.innerHTML = `
            <p><strong>You:</strong> ${question}</p>
            <p><strong>ALVIN:</strong></p>
            <ul>
                ${data.answer
                    .split("\n")
                    .map(line => `<li>${line}</li>`)
                    .join("")}
            </ul>
        `;

    } catch {
        conversation.innerHTML = `
            <p><strong>You:</strong> ${question}</p>
            <p><strong>ALVIN:</strong> The server is not responding. Please try again.</p>
        `;
    }
};
