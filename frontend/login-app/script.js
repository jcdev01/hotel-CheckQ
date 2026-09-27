const API_URL = 'http://127.0.0.1:8000';

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('identificacao').value.trim();
    const senha = document.getElementById('senha').value;
    const mensagem = document.getElementById('mensagemFeedback');
    const btn = document.getElementById('submitBtn');

    mensagem.textContent = '';

    if (!email || !senha) {
        mensagem.textContent = 'Preencha o e-mail e a senha.';
        mensagem.style.color = 'red';
        return;
    }

    btn.disabled = true;
    btn.textContent = 'Autenticando...';

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                senha: senha
            })
        });

        const dados = await response.json();

        if (response.ok) {
            localStorage.setItem('hospede_logado', dados.nome);
            localStorage.setItem('token', dados.token);

            window.location.href = '../checkin-app/index.html';
        } else {
            mensagem.textContent = dados.detail || 'E-mail ou senha incorretos.';
            mensagem.style.color = 'red';
        }

    } catch (error) {
        console.error('Erro no login:', error);

        mensagem.textContent = 'Erro de conexão com o servidor da API.';
        mensagem.style.color = 'red';

    } finally {
        btn.disabled = false;
        btn.textContent = 'Entrar no Sistema';
    }
});

