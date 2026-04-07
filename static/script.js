// === ЧАТ ===
const chatInput = document.getElementById("chat-input");
const chatBox = document.getElementById("chat-box");

function sendMessage() {
    if (!chatInput.value) return;

    const msg = document.createElement("div");
    msg.className = "panel";
    msg.innerText = "👤: " + chatInput.value;

    chatBox.appendChild(msg);
    chatInput.value = "";

    chatBox.scrollTop = chatBox.scrollHeight;
}

// Enter отправка
if (chatInput) {
    chatInput.addEventListener("keypress", function(e) {
        if (e.key === "Enter") sendMessage();
    });
}

// === КУБИК (операционная) ===
function rollDice() {
    const diceEl = document.getElementById("dice");

    let rolls = 10;
    let interval = setInterval(() => {
        diceEl.innerText = Math.floor(Math.random() * 6) + 1;
        rolls--;

        if (rolls <= 0) {
            clearInterval(interval);
        }
    }, 100);
}

// === ПОИСК ПАЦИЕНТОВ ===
function searchPatients() {
    const input = document.getElementById("search").value.toLowerCase();
    const patients = document.querySelectorAll(".patient");

    patients.forEach(p => {
        const text = p.innerText.toLowerCase();
        p.style.display = text.includes(input) ? "block" : "none";
    });
}

// === ВЫБОР ПАЦИЕНТА ===
let selectedPatients = [];

function selectPatient(id) {
    const el = document.getElementById("patient-" + id);

    if (selectedPatients.includes(id)) {
        selectedPatients = selectedPatients.filter(p => p !== id);
        el.style.border = "2px solid red";
    } else {
        selectedPatients.push(id);
        el.style.border = "2px solid lime";
    }

    document.getElementById("selected-count").innerText =
        "Выбрано: " + selectedPatients.length;
}

// === АНИМАЦИЯ КНОПОК ===
document.querySelectorAll("button").forEach(btn => {
    btn.addEventListener("mouseover", () => {
        btn.style.transform = "scale(1.05)";
    });
    btn.addEventListener("mouseout", () => {
        btn.style.transform = "scale(1)";
    });
});
