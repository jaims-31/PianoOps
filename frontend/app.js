const API_BASE = "http://localhost:8080";

let currentExercise = null;
let questionStartedAt = null;
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function fetchExercise(clef, difficulty) {
  const response = await fetch(
    `${API_BASE}/api/exercises/exercise?clef=${clef}&difficulty=${difficulty}`,
    { cache: "no-store" }
  );
  if (!response.ok) {
    throw new Error(`Erreur exercises-service: ${response.status}`);
  }
  return response.json();
}

async function submitAnswer(option) {
  const responseTimeMs = Date.now() - questionStartedAt;
  const correctLetter = currentExercise.key.charAt(0).toUpperCase();
  const correct = option.letter === correctLetter;

  await fetch(`${API_BASE}/api/stats/answers`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      exercise_id: currentExercise.id,
      clef: currentExercise.clef,
      note_key: currentExercise.key,
      note_letter: correctLetter,
      given_answer: option.letter,
      correct: correct,
      response_time_ms: responseTimeMs,
    }),
  });

  showFeedback(correct, correctLetter);
  await refreshStats();
  await sleep(1200);
  await loadNextExercise();
}

function showFeedback(correct, correctLetter) {
  const feedback = document.getElementById("feedback");
  feedback.classList.remove("correct", "incorrect");
  if (correct) {
    feedback.textContent = "Correct !";
    feedback.classList.add("correct");
  } else {
    feedback.textContent = `Raté, c'était un ${correctLetter}`;
    feedback.classList.add("incorrect");
  }
}

function renderStaff(exercise) {
  const container = document.getElementById("staff");
  container.innerHTML = "";

  const factory = new VexFlow.Factory({
    renderer: { elementId: "staff", width: 500, height: 200 },
  });

  const system = factory.System({ width: 460 });
  const note = factory.StaveNote({ keys: [exercise.key], duration: "q", clef: exercise.clef });
  const voice = factory.Voice().setStrict(false).addTickables([note]);

  system.addStave({ voices: [voice] }).addClef(exercise.clef);
  factory.draw();
}

function renderAnswerButtons(exercise) {
  const container = document.getElementById("answers");
  container.innerHTML = "";

  exercise.answer_options.forEach((option) => {
    const button = document.createElement("button");
    button.textContent = `${option.letter} (${option.solfege})`;
    button.addEventListener("click", () => submitAnswer(option));
    container.appendChild(button);
  });
}

async function refreshStats() {
  const response = await fetch(`${API_BASE}/api/stats/summary`, { cache: "no-store" });
  const stats = await response.json();
  const content = document.getElementById("stats-content");

  content.innerHTML = `
    <span>Réponses :</span><span>${stats.total_answers}</span>
    <span>Bonnes réponses :</span><span>${stats.correct_answers}</span>
    <span>Précision :</span><span>${stats.accuracy}%</span>
    <span>Série en cours :</span><span>${stats.current_streak}</span>
    <span>Meilleure série :</span><span>${stats.best_streak}</span>
  `;
}

async function loadNextExercise() {
  const clef = document.getElementById("clef-select").value;
  const difficulty = document.getElementById("difficulty-select").value;

  currentExercise = await fetchExercise(clef, difficulty);
  questionStartedAt = Date.now();

  renderStaff(currentExercise);
  renderAnswerButtons(currentExercise);

  const feedback = document.getElementById("feedback");
  feedback.textContent = "";
  feedback.classList.remove("correct", "incorrect");
}

document.getElementById("clef-select").addEventListener("change", loadNextExercise);
document.getElementById("difficulty-select").addEventListener("change", loadNextExercise);

VexFlow.loadFonts("Bravura", "Academico").then(() => {
  VexFlow.setFonts("Bravura", "Academico");
  loadNextExercise();
  refreshStats();
});
