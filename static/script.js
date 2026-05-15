<script>

let money = 100;
let diamonds = 10;
let xp = 0;
let level = 1;

// СТАТУС
function showStatus(text,color="lime"){

    let status = document.getElementById("status");

    status.innerText = text;
    status.style.color = color;
}

// РЕГИСТРАЦИЯ
function register(){

    let name =
        document.getElementById("loginName").value.trim();

    let pass =
        document.getElementById("loginPassword").value.trim();

    if(name === "" || pass === ""){

        showStatus("Введите логин и пароль","red");
        return;
    }

    localStorage.setItem("rp_name",name);
    localStorage.setItem("rp_pass",pass);

    showStatus("Аккаунт создан");
}

// ВХОД
function login(){

    let name =
        document.getElementById("loginName").value.trim();

    let pass =
        document.getElementById("loginPassword").value.trim();

    let savedName = localStorage.getItem("rp_name");
    let savedPass = localStorage.getItem("rp_pass");

    if(savedName === null){

        showStatus("Сначала зарегистрируйтесь","orange");
        return;
    }

    if(name === savedName && pass === savedPass){

        document.getElementById("loginScreen").style.display="none";

        document.getElementById("game").style.display="block";

        document.getElementById("playerName").innerText=name;

        return;
    }

    showStatus("Неверный логин или пароль","red");
}

// XP
function update(){

    level = Math.floor(xp / 100) + 1;

    document.getElementById("money").innerText = money;
    document.getElementById("diamonds").innerText = diamonds;
    document.getElementById("xp").innerText = xp;
    document.getElementById("level").innerText = level;

    document.getElementById("xpBar").style.width =
        (xp % 100) + "%";
}

// ПАЦИЕНТЫ
function loadPatients(){

    let box = document.getElementById("patients");
    box.innerHTML = "";

    for(let i=1;i<=100;i++){

        let div = document.createElement("div");
        div.className = "item";

        div.innerHTML = `
            🧑 Пациент #${i}
            <div class="progress">
                <div class="bar" id="b${i}"></div>
            </div>
        `;

        div.onclick = ()=>heal(i);

        box.appendChild(div);
    }
}

// ЛЕЧЕНИЕ
function heal(id){

    let bar = document.getElementById("b"+id);

    if(!bar) return;

    let progress = 0;

    let timer = setInterval(()=>{

        progress += 10;

        bar.style.width = progress + "%";

        if(progress >= 100){

            clearInterval(timer);

            money += 20;
            xp += 15;

            update();

            bar.style.background = "lime";
        }

    },300);
}

// ЧАТ
function sendMessage(){

    let input = document.getElementById("chatInput");
    let chat = document.getElementById("chat");

    if(input.value.trim()=="") return;

    let div = document.createElement("div");
    div.className = "msg";

    div.innerText =
        document.getElementById("playerName").innerText +
        ": " + input.value;

    chat.appendChild(div);

    input.value = "";

    chat.scrollTop = chat.scrollHeight;
}

update();

</script>
