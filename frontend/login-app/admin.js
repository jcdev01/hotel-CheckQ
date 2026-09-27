const API_URL = 'http://127.0.0.1:8000';

document.getElementById('adminLoginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const usuario = document.getElementById('usuario').value.trim();
    const senha = document.getElementById('senha').value;
    const mensagem = document.getElementById('mensagemFeedback');
    const btn = document.getElementById('submitBtn');

    btn.disabled = true;
    btn.textContent = 'Autenticando...';
    mensagem.textContent = '';

    try {
        const response = await fetch(`${API_URL}/admin/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: usuario, password: senha })
        });

        if (response.ok) {
            localStorage.setItem('admin_logado', 'true');
            window.location.href = '../checkin-recepcao/checkin_recepcao.html';
        } else {
            mensagem.textContent = 'Usuário ou senha incorretos.';
            mensagem.style.color = 'red';
        }
    } catch (error) {
        console.error(error);
        mensagem.textContent = 'Erro de conexão com o servidor da API.';
        mensagem.style.color = 'red';
    } finally {
        btn.disabled = false;
        btn.textContent = 'Entrar';
    }
});