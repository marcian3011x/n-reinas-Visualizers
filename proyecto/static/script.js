const startBtn = document.getElementById("startBtn");
const nInput = document.getElementById("nInput");
const boardEl = document.getElementById("board");
const genCounter = document.getElementById("genCounter");

startBtn.addEventListener("click", async () => {
  const n = parseInt(nInput.value);

  const response = await fetch("/solve", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ n })
  });

  const data = await response.json();
  animateHistory(data.boards_history, n);
});

function renderBoard(board, n) {
  boardEl.style.gridTemplateColumns = `repeat(${n}, 40px)`;
  boardEl.innerHTML = "";

  for (let row = 0; row < n; row++) {
    for (let col = 0; col < n; col++) {
      const cell = document.createElement("div");
      cell.className = `cell ${(row + col) % 2 === 0 ? "light" : "dark"}`;
      if (board[col] === row) {
        cell.textContent = "♛";
      }
      boardEl.appendChild(cell);
    }
  }
}

function animateHistory(history, n) {
  let gen = 0;
  const interval = setInterval(() => {
    if (gen >= history.length) {
      clearInterval(interval);
      return;
    }
    renderBoard(history[gen], n);
    genCounter.textContent = `Generación: ${gen + 1} / ${history.length}`;
    gen++;
  }, 500);
}