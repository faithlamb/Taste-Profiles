// Detect which page we are on
const currentPage = window.location.pathname;

// Taste profiles
const profiles = [
    "Local Loyalist",
    "Trend Chaser",
    "Culinary Purist",
    "Comfort Seeker",
    "Adventurous Explorer",
    "Social Foodie"
];

// QUIZ DATA — add all 10 questions here
// (I will help you paste the full set next if you want)
const quizData = [
    {
        question: "When you're choosing a restaurant in a new city, what's your first instinct?",
        answers: [
            { text: "Find the spot locals swear by", profile: "Local Loyalist" },
            { text: "Go for the trend everyone's posting on TikTok", profile: "Trend Chaser" },
            { text: "Pick something upscale and chef-driven", profile: "Culinary Purist" },
            { text: "Look for a cozy, comforting classic", profile: "Comfort Seeker" },
            { text: "Try something totally unfamiliar", profile: "Adventurous Explorer" },
            { text: "Pick a place that’s lively and perfect for sharing plates with friends", profile: "Social Foodie" }
        ]
    },
    {
        question: "What's your ideal dining vibe?",
        answers: [
            { text: "Casual, loud, communal", profile: "Social Foodie" },
            { text: "Sleek, modern, minimalist", profile: "Trend Chaser" },
            { text: "Romantic or intimate", profile: "Culinary Purist" },
            { text: "Nostalgic and homey", profile: "Comfort Seeker" },
            { text: "Adventurous and surprising", profile: "Adventurous Explorer" },
            { text: "A neighborhood spot with character and a loyal crowd", profile: "Local Loyalist" }
        ]
    },
    {
        question: "Which dish would you choose on a random Tuesday night?",
        answers: [
            { text: "A perfectly executed burger or taco", profile: "Social Foodie" },
            { text: "A seasonal tasting menu dish", profile: "Culinary Purist" },
            { text: "A comforting bowl of pasta or soup", profile: "Comfort Seeker" },
            { text: "Something spicy or globally inspired", profile: "Adventurous Explorer" },
            { text: "Whatever's trending on food Instagram", profile: "Trend Chaser" },
            { text: "A classic regional specialty that locals swear by", profile: "Local Loyalist" }
        ]
    },
    {
        question: "How do you feel about waiting in line for food?",
        answers: [
            { text: "Worth it if the food is legendary", profile: "Culinary Purist" },
            { text: "Only if the place is the hot spot", profile: "Trend Chaser" },
            { text: "Prefer reservations and planning", profile: "Comfort Seeker" },
            { text: "I'd rather go somewhere low-key", profile: "Local Loyalist" },
            { text: "I'll wait if the experience is unique", profile: "Adventurous Explorer" },
            { text: "I don’t mind if I’m with friends — it’s part of the fun", profile: "Social Foodie" }
        ]
    },
    {
        question: "What's your relationship with spice?",
        answers: [
            { text: "Mild and comforting", profile: "Comfort Seeker" },
            { text: "Medium heat", profile: "Social Foodie" },
            { text: "Bring on the fire", profile: "Adventurous Explorer" },
            { text: "Depends on the cuisine", profile: "Culinary Purist" },
            { text: "I'll try anything once", profile: "Trend Chaser" },
            { text: "I like whatever the local crowd prefers", profile: "Local Loyalist" }
        ]
    },
    {
        question: "What's your go-to drink pairing?",
        answers: [
            { text: "Craft beer or natural wine", profile: "Local Loyalist" },
            { text: "Classic cocktails", profile: "Social Foodie" },
            { text: "Trendy drinks (espresso martinis, etc.)", profile: "Trend Chaser" },
            { text: "Tea, soda, or something non-alcoholic", profile: "Comfort Seeker" },
            { text: "Whatever the house specialty is", profile: "Culinary Purist" },
            { text: "Something I’ve never tried before — surprise me", profile: "Adventurous Explorer" }
        ]
    },
    {
        question: "When traveling, what excites you most about a city's food scene?",
        answers: [
            { text: "Iconic local staples", profile: "Social Foodie" },
            { text: "High-end restaurants and chefs", profile: "Culinary Purist" },
            { text: "Hidden gems only locals know", profile: "Local Loyalist" },
            { text: "Cultural diversity and global flavors", profile: "Adventurous Explorer" },
            { text: "Viral spots and aesthetic cafés", profile: "Trend Chaser" },
            { text: "Familiar dishes that feel like home, even in a new place", profile: "Comfort Seeker" }
        ]
    },
    {
        question: "What's your ordering style?",
        answers: [
            { text: "Share everything", profile: "Social Foodie" },
            { text: "Stick to your favorites", profile: "Comfort Seeker" },
            { text: "Ask the server for recommendations", profile: "Local Loyalist" },
            { text: "Try the most unusual item", profile: "Adventurous Explorer" },
            { text: "Order what photographs well", profile: "Trend Chaser" },
            { text: "I choose the dish that best showcases the chef’s technique", profile: "Culinary Purist" }
        ]
    },
    {
        question: "Which food media do you trust most?",
        answers: [
            { text: "Eater city guides", profile: "Comfort Seeker" },
            { text: "Bon Appétit or chef interviews", profile: "Culinary Purist" },
            { text: "Local blogs and word-of-mouth", profile: "Local Loyalist" },
            { text: "TikTok creators", profile: "Trend Chaser" },
            { text: "Friend recommendations", profile: "Social Foodie" },
            { text: "Any source that highlights bold, off-the-beaten-path eats", profile: "Adventurous Explorer" }
        ]
    },
    {
        question: "What matters most in a restaurant recommendation?",
        answers: [
            { text: "Authenticity", profile: "Local Loyalist" },
            { text: "Creativity", profile: "Social Foodie" },
            { text: "Comfort", profile: "Comfort Seeker" },
            { text: "Novelty", profile: "Adventurous Explorer" },
            { text: "Aesthetic + vibe", profile: "Trend Chaser" },
            { text: "Precision and mastery — I want the highest quality execution", profile: "Culinary Purist" }
        ]
    }
];


// ------------------------------
// QUIZ PAGE LOGIC
// ------------------------------
if (currentPage.includes("quiz.html")) {
    const quizContainer = document.getElementById("quiz-container");

    // Render quiz
    quizData.forEach((q, index) => {
        const questionDiv = document.createElement("div");
        questionDiv.classList.add("question-block");

        const questionText = document.createElement("h3");
        questionText.textContent = `${index + 1}. ${q.question}`;
        questionDiv.appendChild(questionText);

        q.answers.forEach(answer => {
            const label = document.createElement("label");
            label.innerHTML = `
                <input type="radio" name="question${index}" value="${answer.profile}">
                ${answer.text}
            `;
            questionDiv.appendChild(label);
        });

        quizContainer.appendChild(questionDiv);
    });

    // Submit button logic
    document.getElementById("submit-btn").addEventListener("click", () => {
        let scores = {
            "Local Loyalist": 0,
            "Trend Chaser": 0,
            "Culinary Purist": 0,
            "Comfort Seeker": 0,
            "Adventurous Explorer": 0,
            "Social Foodie": 0
        };

        quizData.forEach((q, index) => {
            const selected = document.querySelector(`input[name="question${index}"]:checked`);
            if (selected) {
                scores[selected.value]++;
            }
        });

        // Save scores for results page
        localStorage.setItem("quizScores", JSON.stringify(scores));

        // Redirect to results
        window.location.href = "results.html";
    });
}

// ------------------------------
// RESULTS PAGE LOGIC
// ------------------------------
if (currentPage.includes("results.html")) {
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
}
