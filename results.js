const scoreList = document.getElementById("score-list");
const scores = JSON.parse(localStorage.getItem("quizScores")) || {};

if (!Object.keys(scores).length) {
    const emptyState = document.createElement("p");
    emptyState.className = "results-empty";
    emptyState.textContent = "No quiz results found yet. Take the quiz to see your scores.";
    scoreList.appendChild(emptyState);
}

for (const profile in scores) {
    const card = document.createElement("a");

    // Convert profile name to matching HTML file
    const fileName = profile.toLowerCase().replace(/ /g, "-") + ".html";

    const percentage = Math.round((scores[profile] / 10) * 100);

    card.className = "profile-card results-card";
    card.href = fileName;
    card.innerHTML = `
        <span class="profile-card-kicker">Quiz Result</span>
        <h3>${profile}</h3>
        <p class="profile-score">Match Score: ${percentage}%</p>
        <span class="profile-card-cta">Explore this profile</span>
    `;

    scoreList.appendChild(card);
}
