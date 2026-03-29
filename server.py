{% extends "base.html" %}

{% block content %}

<h3>💬 Чат больницы</h3>

<div class="card">

<form method="post">
    <input name="msg" placeholder="Написать сообщение..." required>
    <button type="submit">Отправить</button>
</form>

</div>

<div class="card">

{% if msgs %}
    {% for m in msgs %}
        <p>🗨 {{ m[0] }}</p>
    {% endfor %}
{% else %}
    <p>❌ Сообщений пока нет</p>
{% endif %}

</div>

{% endblock %}
