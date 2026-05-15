<script>

// ONLINE
document.getElementById("online").innerText = Math.floor(Math.random()*50+10);

// XP BAR
let xp = 120;
document.getElementById("xpBar").style.width = (xp/5) + "%";

// PATIENTS
function loadPatients(){
    let sel = document.getElementById("patientSelect");
    sel.innerHTML = "";

    for(let i=1;i<=50;i++){
        let opt = document.createElement("option");
        opt.text = "Пациент #" + i;
        sel.add(opt);
    }

    alert("Пациенты загружены");
}

function callPatient(){
    let sel = document.getElementById("patientSelect");
    alert("Пациент вызван: " + sel.value);
}

// AMBULANCE
function callAmbulance(){
    alert("🚑 Скорая выехала!");
}

// DICE
function rollDice(){
    let r = Math.floor(Math.random()*6)+1;
    document.getElementById("dice").innerText = "Результат: " + r;
}

// ALLIANCE (фикс экономики)
function createAlliance(){
    alert("🤝 Союз создан (−500 💎)");
}

// LAB
function takeSample(){
    alert("🧪 Образец взят");
}

function takeAnalysis(){
    alert("📊 Анализ взят");
}

// DOCTOR
function openDoctor(){
    alert("👨‍⚕️ Кабинет открыт");
}

// SEARCH (ВАЖНО: теперь правильно читаем input)
function searchAll(){

    let player = document.getElementById("searchPlayer").value;
    let alliance = document.getElementById("searchAlliance").value;
    let patient = document.getElementById("searchPatient").value;

    alert(
        "🔍 Поиск\n" +
        "Игрок: " + player + "\n" +
        "Союз: " + alliance + "\n" +
        "Пациент: " + patient
    );
}

// CHAT
function sendMessage(){

    let input = document.getElementById("chatInput");
    let chat = document.getElementById("chat");

    if(input.value.trim() === "") return;

    let msg = document.createElement("div");
    msg.className = "msg";
    msg.innerText = "Игрок: " + input.value;

    chat.appendChild(msg);

    input.value = "";
    chat.scrollTop = chat.scrollHeight;
}

</script>
