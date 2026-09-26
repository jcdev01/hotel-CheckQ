const API_URL = 'http://127.0.0.1:8000';

document.getElementById('cadastroForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const btn = document.getElementById('submitBtn');
    const mensagem = document.getElementById('mensagemFeedback');
    
    btn.disabled = true;
    btn.textContent = 'Cadastrando...';

    const payload = {
        nome: document.getElementById('nome').value.trim(),
        cpf: document.getElementById('cpf').value.trim(),
        email: document.getElementById('email').value.trim(),
        telefone: document.getElementById('telefone').value.trim(),
        data_nascimento: document.getElementById('data_nascimento').value + "T00:00:00",
        senha: document.getElementById('senha').value
    };

    try {
        const response = await fetch(`${API_URL}/usuarios`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            mensagem.textContent = 'Conta criada com sucesso! Redirecionando...';
            mensagem.style.color = 'green';
            
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 2000);
        } else {
            const erro = await response.json();
            mensagem.textContent = erro.detail || 'Erro ao realizar cadastro.';
            mensagem.style.color = 'red';
        }
    } catch (error) {
        console.error(error);
        mensagem.textContent = 'Erro de conexão com o servidor.';
        mensagem.style.color = 'red';
    } finally {
        if (!response?.ok) {
            btn.disabled = false;
            btn.textContent = 'Criar Conta';
        }
    }
})