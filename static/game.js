document.addEventListener("DOMContentLoaded", () => {

    // =====================
    // 🎲 КУБИК
    // =====================
    const diceBtn = document.getElementById("diceBtn");
    const diceBox = document.getElementById("dice");

    if (diceBtn) {
        diceBtn.addEventListener("click", () => {
            const r = Math.floor(Math.random() * 6) + 1;
            if (diceBox) diceBox.innerText = "Результат: " + r;
        });
    }

    // =====================
    // 🤝 СОЮЗ
    // =====================
    const allianceBtn = document.getElementById("allianceBtn");

    if (allianceBtn) {
        allianceBtn.addEventListener("click", () => {
            alert("🤝 Союз создан (−500 💎)");
        });
    }

    // =====================
    // 🚑 СКОРАЯ
    // =====================
    const ambulanceBtn = document.getElementById("ambulanceBtn");

    if (ambulanceBtn) {
        ambulanceBtn.addEventListener("click", () => {
            alert("🚑 Скорая выехала!");
        });
    }

    // =====================
    // 🧑‍🤝‍🧑 ПАЦИЕНТЫ
    // =====================
    const patientBtn = document.getElementById("loadPatientsBtn");
    const patientSelect = document.getElementById("patientSelect");

    if (patientBtn) {
        patientBtn.addEventListener("click", () => {
            if (!patientSelect) return;

            patientSelect.innerHTML = "";

            for (let i = 1; i <= 50; i++) {
                let opt = document.createElement("option");
                opt.textContent = "Пациент #" + i;
                patientSelect.appendChild(opt);
            }

            alert("Пациенты загружены");
        });
    }

    const callPatientBtn = document.getElementById("callPatientBtn");

    if (callPatientBtn) {
        callPatientBtn.addEventListener("click", () => {
            alert("Вызван: " + patientSelect.value);
        });
    }

    // =====================
    // 🧪 ЛАБА
    // =====================
    const sampleBtn = document.getElementById("sampleBtn");
    const analysisBtn = document.getElementById("analysisBtn");

    if (sampleBtn) {
        sampleBtn.addEventListener("click", () => {
            alert("🧪 Образец взят");
        });
    }

    if (analysisBtn) {
        analysisBtn.addEventListener("click", () => {
            alert("📊 Анализ выполнен");
        });
    }

    // =====================
    // 👨‍⚕️ КАБИНЕТ
    // =====================
    const doctorBtn = document.getElementById("doctorBtn");

    if (doctorBtn) {
        doctorBtn.addEventListener("click", () => {
            alert("👨‍⚕️ Кабинет открыт");
        });
    }

    // =====================
    // 💬 ЧАТ
    // =====================
    const chatBtn = document.getElementById("chatBtn");
    const chatInput = document.getElementById("chatInput");
    const chatBox = document.getElementById("chat");

    if (chatBtn) {
        chatBtn.addEventListener("click", () => {
            if (!chatInput || !chatBox) return;

            if (chatInput.value.trim() === "") return;

            const msg = document.createElement("div");
            msg.className = "msg";
            msg.textContent = "Игрок: " + chatInput.value;

            chatBox.appendChild(msg);

            chatInput.value = "";
            chatBox.scrollTop = chatBox.scrollHeight;
        });
    }

});
