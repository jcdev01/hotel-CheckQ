const API_URL = 'http://127.0.0.1:8000';

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const identificacao = document.getElementById('identificacao').value.trim();
    const senha = document.getElementById('senha').value;
    const mensagem = document.getElementById('mensagemFeedback');
    const btn = document.getElementById('submitBtn');

    btn.disabled = true;
    btn.textContent = 'Autenticando...';

    try {
        if (identificacao.toLowerCase() === 'admin' || identificacao.toLowerCase() === 'jubileu') {
            const response = await fetch(`${API_URL}/admin/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: identificacao, senha: senha })
            });

            if (response.ok) {
                localStorage.setItem('admin_logado', 'true');
                window.location.href = '../checkin-recepcao/checkin_recepcao.html';
            } else {
                mensagem.textContent = 'Senha de administrador incorreta.';
                mensagem.style.color = 'red';
            }
        } 
        else {
            const response = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: identificacao, senha: senha })
            });

            if (response.ok) {
                const dados = await response.json();
                localStorage.setItem('hospede_logado', dados.nome);
                window.location.href = '../checkin-app/index.html';
            } else {
                mensagem.textContent = 'E-mail ou senha incorretos.';
                mensagem.style.color = 'red';
            }
        }
    } catch (error) {
        console.error(error);
        mensagem.textContent = 'Erro de conexao com o servidor da API.';
        mensagem.style.color = 'red';
    } finally {
        btn.disabled = false;
        btn.textContent = 'Entrar no Sistema';
    }
});