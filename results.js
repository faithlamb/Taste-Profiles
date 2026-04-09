const scoreList = document.getElementById("score-list");
const scores = JSON.parse(localStorage.getItem("quizScores"));

for (const profile in scores) {
    const li = document.createElement("li");

    // Convert profile name to matching HTML file
    const fileName = profile.toLowerCase().replace(/ /g, "-") + ".html";

    li.innerHTML = `
        <a href="${fileName}">${profile}</a>: ${scores[profile]} points
    `;

    scoreList.appendChild(li);
}
