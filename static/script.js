
document.addEventListener("DOMContentLoaded", () => {
    const moneyEl = document.getElementById("money");
    const expEl = document.getElementById("exp");
    const diamondsEl = document.getElementById("diamonds");
    const chatBox = document.getElementById("chat_box");
    const chatInput = document.getElementById("chat_input");
    const sceneEl = document.getElementById("scene");

    const updateUI = (state) => {
        moneyEl.textContent = `💰 Деньги: ${state.money}`;
        expEl.textContent = `⭐ Опыт: ${state.exp}`;
        diamondsEl.textContent = `💎 Алмазы: ${state.diamonds}`;
        chatBox.innerHTML = state.chat.map(msg => `<div class="chat_msg">${msg}</div>`).join("");
        chatBox.scrollTop = chatBox.scrollHeight;

        let sceneHTML = "";
        if(state.location === "lobby") {
            sceneHTML = `<img src="/static/images/doctor.png" class="scene-img"><p>Вы находитесь в лобби.</p>`;
        } else if(state.location === "room") {
            sceneHTML = `<img src="/static/images/room.png" class="scene-img"><p>Вы в кабинете. Можно лечить пациентов.</p>`;
        } else if(state.location === "lab") {
            sceneHTML = `<img src="/static/images/lab.png" class="scene-img"><p>Вы в лаборатории. Можно делать анализы.</p>`;
        }
        sceneEl.innerHTML = sceneHTML;
    }

    const sendAction = (type) => {
        fetch("/action", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({type})
        })
        .then(res => res.json())
        .then(data => updateUI(data.state));
    }

    document.getElementById("treat").addEventListener("click", () => sendAction("treat_patient"));
    document.getElementById("lab").addEventListener("click", () => sendAction("lab_test"));
    document.querySelectorAll(".location-btn").forEach(btn => {
        btn.addEventListener("click", () => sendAction(btn.dataset.action));
    });

    document.getElementById("send_msg").addEventListener("click", () => {
        const text = chatInput.value.trim();
        if (!text) return;

        fetch("/send_message", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({text})
        })
        .then(res => res.json())
        .then(data => {
            chatBox.innerHTML = data.chat.map(msg => `<div class="chat_msg">${msg}</div>`).join("");
            chatBox.scrollTop = chatBox.scrollHeight;
            chatInput.value = "";
        });
    });
});
