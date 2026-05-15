// ЖДЁМ загрузку страницы (очень важно)
document.addEventListener("DOMContentLoaded", function () {

    // ONLINE
    const online = document.getElementById("online");
    if (online) online.innerText = Math.floor(Math.random() * 50 + 10);

    // XP BAR
    const xpBar = document.getElementById("xpBar");
    if (xpBar) xpBar.style.width = "30%";

});

// 🎲 КУБИК
function rollDice() {
    const dice = document.getElementById("dice");
    if (!dice) return;

    const r = Math.floor(Math.random() * 6) + 1;
    dice.innerText = "Результат: " + r;
}

// 🤝 СОЮЗ
function createAlliance() {
    alert("Союз создан (−500 💎)");
}

// 🧑‍🤝‍🧑 ПАЦИЕНТЫ
function loadPatients() {
    const sel = document.getElementById("patientSelect");
    if (!sel) return;

    sel.innerHTML = "";

    for (let i = 1; i <= 50; i++) {
        let opt = document.createElement("option");
        opt.textContent = "Пациент #" + i;
        sel.appendChild(opt);
    }

    alert("Пациенты загружены");
}

function callPatient() {
    const sel = document.getElementById("patientSelect");
    if (!sel) return;

    alert("Вызван: " + sel.value);
}

// 🚑 СКОРАЯ
function callAmbulance() {
    alert("🚑 Скорая выехала");
}

// 🧪 ЛАБА
function takeSample() {
    alert("Образец взят");
}

function takeAnalysis() {
    alert("Анализ взят");
}

// 👨‍⚕️ КАБИНЕТ
function openDoctor() {
    alert("Кабинет открыт");
}

// 🔍 ПОИСК (ИСПРАВЛЕНО)
function searchAll() {
    const player = document.getElementById("searchPlayer")?.value || "";
    const alliance = document.getElementById("searchAlliance")?.value || "";
    const patient = document.getElementById("searchPatient")?.value || "";

    alert(
        "Поиск:\n" +
        "Игрок: " + player + "\n" +
        "Союз: " + alliance + "\n" +
        "Пациент: " + patient
    );
}

// 💬 ЧАТ
function sendMessage() {
    const input = document.getElementById("chatInput");
    const chat = document.getElementById("chat");

    if (!input || !chat) return;
    if (input.value.trim() === "") return;

    const msg = document.createElement("div");
    msg.className = "msg";
    msg.textContent = "Игрок: " + input.value;

    chat.appendChild(msg);

    input.value = "";
    chat.scrollTop = chat.scrollHeight;
}
