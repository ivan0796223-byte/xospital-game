
{% extends "base.html" %}
{% block content %}

<style>
.car-card{
    background:#222;
    padding:12px;
    margin:10px;
    border-radius:12px;
}

.car-icon{
    width:70px;
    height:70px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:34px;
    margin:auto;
    box-shadow:0 0 12px red;
    background:#111;
}

.status-free{color:lime}
.status-busy{color:orange}
.status-call{color:red}
</style>

<h2>🚑 Автопарк</h2>

<a href="/new_call">
    <button>📞 Новый вызов</button>
</a>

<!-- 📍 ВЫЗОВЫ -->
<div class="box">
<h3>📍 Вызовы</h3>

{% if car_calls %}
    {% for c in car_calls %}
        <p class="status-call">👤 {{ c.patient }} | ⚠️ Срочность: {{ c.severity }}</p>
    {% endfor %}
{% else %}
    <p>Нет вызовов</p>
{% endif %}
</div>

<!-- 🚑 МАШИНЫ -->
<div class="box">
<h3>🚑 Машины</h3>

{% for car, status in car_status.items() %}

<div class="car-card">

    <div class="car-icon">🚑</div>

    <p><b>{{ car }}</b></p>

    {% if "свободна" in status %}
        <p class="status-free">🟢 {{ status }}</p>
    {% elif "в пути" in status %}
        <p class="status-busy">🟠 {{ status }}</p>
    {% else %}
        <p>{{ status }}</p>
    {% endif %}

    <form method="POST" action="/send_car">
        <input type="hidden" name="car" value="{{ car }}">
        <button>🚨 Отправить</button>
    </form>

    <form method="POST" action="/return_car">
        <input type="hidden" name="car" value="{{ car }}">
        <button>🏥 Вернулась</button>
    </form>

</div>

{% endfor %}
</div>

{% endblock %}
