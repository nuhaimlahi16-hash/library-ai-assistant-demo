const input = document.getElementById("questionInput");
const askBtn = document.getElementById("askBtn");
const answerEl = document.getElementById("answer");
const userQ = document.getElementById("userQuestion");

askBtn.onclick = async () => {
    const text = input.value.trim();
    if (!text) return;

    userQ.textContent = text;
    answerEl.textContent = "Loading...";

    try {
        const res = await fetch("http://127.0.0.1:8000/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: text })
        });

        const data = await res.json();
        answerEl.textContent = data.answer || "No answer available.";

    } catch {
        answerEl.textContent = "Server not responding.";
    }
};
