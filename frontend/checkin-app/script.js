const API_URL = 'http://127.0.0.1:8000';

document.getElementById('checkinForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const btn = document.getElementById('submitBtn');
    const mensagem = document.getElementById('mensagemFeedback');
    btn.disabled = true;
    btn.textContent = 'Enviando...';

    // objeto com os dados do form
    const payload = {
        nome_hospede: document.getElementById('nome_hospede').value,
        numero_quarto: parseInt(document.getElementById('numero_quarto').value),
        horario_entrada: document.getElementById('horario_entrada').value,
        horario_saida: document.getElementById('horario_saida').value
    };

    try {
        const response = await fetch(`${API_URL}/fila`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            mensagem.textContent = 'Check-in solicitado com sucesso! Aguarde na recepção.';
            mensagem.style.color = 'green';
            document.getElementById('checkinForm').reset();
        } else if (response.status === 409) {
            mensagem.textContent = 'Erro: Este quarto já está ocupado!';
            mensagem.style.color = 'red';
        } else {
            mensagem.textContent = 'Erro ao processar solicitação.';
            mensagem.style.color = 'red';
        }
    } catch (error) {
        console.error(error);
        mensagem.textContent = 'Erro de conexão com o servidor. Verifique se a API está rodando.';
        mensagem.style.color = 'red';
    } finally {
        btn.disabled = false;
        btn.textContent = 'Entrar na Fila';
    }
    


});