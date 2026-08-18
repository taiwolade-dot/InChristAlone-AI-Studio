
function animateScore(target){
    let current = parseInt(scoreEl.textContent || "0");

    const timer = setInterval(() => {
        if(current >= target){
            clearInterval(timer);
            return;
        }
        current++;
        scoreEl.textContent = current;
    }, 40);
}

const statusEl = document.getElementById("status");
const quizArea = document.getElementById("quiz-area");
const questionNumberEl = document.getElementById("question-number");
const questionTextEl = document.getElementById("question-text");
const timerEl = document.getElementById("timer");
const answersEl = document.getElementById("answers");
const resultEl = document.getElementById("result");
const progressFill = document.getElementById("progress-fill");
const scoreEl = document.getElementById("score");
const leaderboardEl = document.getElementById("leaderboard-list");

async function loadState() {
    try {
        const response = await fetch(`/api/bible-quiz/session/${sessionId}/state`);
        if (!response.ok) throw new Error(response.status);

        const data = await response.json();

        statusEl.textContent = "Status: " + data.status;

        if (data.status === "active" && data.question) {
            quizArea.style.display = "block";

            questionNumberEl.textContent =
                `Question ${data.current_question_index + 1} of ${data.total_questions}`;

            questionTextEl.textContent = data.question.text;

            timerEl.textContent =
                `⏱ ${data.question.seconds} seconds`;

            answersEl.innerHTML = "";

            data.question.options.forEach((option, index) => {
                const btn = document.createElement("button");
                const labels = ["A","B","C","D"];

                btn.innerHTML = `<strong>${labels[index]}.</strong> ${option}`;
                btn.className = "answer-btn";
                btn.disabled = false;

                btn.onclick = async () => {
                    document.querySelectorAll(".answer-btn").forEach(b => b.disabled = true);

                    const res = await fetch(`/bible-quiz/session/${sessionId}/answer`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            chosen_index: index,
                            time_taken_ms: 0
                        })
                    });

                    const result = await res.json();

                    if(result.is_correct){
                        btn.classList.add("correct");
                        resultEl.textContent = "✅ Correct!";
                    }else{
                        btn.classList.add("wrong");
                        resultEl.textContent = "❌ Wrong!";
                    }

                    if(result.score !== undefined){
                        animateScore(result.score);
                    }
                };
                answersEl.appendChild(btn);
            });

        } else {
            quizArea.style.display = "none";
        }

        scoreEl.textContent = 0;

        leaderboardEl.innerHTML = "";

        data.leaderboard.forEach((player, i) => {
            const row = document.createElement("div");
            row.textContent =
                `${i===0?"🥇":i===1?"🥈":i===2?"🥉":"🏅"} ${player.name} — ${player.score} pts`;
            leaderboardEl.appendChild(row);
        });

    } catch (err) {
        console.error(err);
        statusEl.textContent = "Connection error";
    }
}

loadState();
setInterval(loadState, 1000);
