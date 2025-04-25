document.getElementById("mathForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const question = document.getElementById("question").value;
    const responseContainer = document.getElementById("response-container");
    const answerElement = document.getElementById("answer");

    const response = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
    });

    const data = await response.json();
    const answer = data.answer;

    answerElement.innerHTML = answer;
    MathJax.Hub.Queue(["Typeset", MathJax.Hub, answerElement]);  // Render LaTeX
});
