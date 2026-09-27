const API_URL = 'http://127.0.0.1:8000';

const welcomeScreen = document.getElementById('welcomeScreen');
const checkinScreen = document.getElementById('checkinScreen');
const startCheckinBtn = document.getElementById('startCheckinBtn');
const backBtn = document.getElementById('backBtn');
const logoutBtn = document.getElementById('logoutBtn');

const nomeUsuario = localStorage.getItem('hospede_logado');

document.getElementById('nomeUsuario').textContent =
    nomeUsuario || 'hóspede';

const checkinForm = document.getElementById('checkinForm');
const submitBtn = document.getElementById('submitBtn');
const mensagem = document.getElementById('mensagemFeedback');

function showCheckinScreen() {
    welcomeScreen.classList.add('hidden');
    checkinScreen.classList.remove('hidden');
    document.getElementById('nome_hospede').focus();
}

function showWelcomeScreen() {
    checkinScreen.classList.add('hidden');
    welcomeScreen.classList.remove('hidden');
    mensagem.textContent = '';
}

startCheckinBtn.addEventListener('click', showCheckinScreen);
backBtn.addEventListener('click', showWelcomeScreen);
logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('hospede_logado');

    window.location.href = '../login-app/index.html';
});

checkinForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    submitBtn.disabled = true;
    submitBtn.textContent = 'Enviando...';
    mensagem.textContent = '';

    const payload = {
        nome_hospede: document.getElementById('nome_hospede').value,
        numero_quarto: parseInt(document.getElementById('numero_quarto').value),
        horario_entrada: document.getElementById('horario_entrada').value,
        horario_saida: document.getElementById('horario_saida').value
    };

    try {
        const response = await fetch(`${API_URL}/fila`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            mensagem.textContent =
                'Check-in solicitado com sucesso! Aguarde na recepção.';
            mensagem.style.color = 'var(--success)';
            checkinForm.reset();
        } else if (response.status === 409) {
            mensagem.textContent = 'Erro: Este quarto já está ocupado!';
            mensagem.style.color = 'var(--error)';
        } else {
            mensagem.textContent = 'Erro ao processar solicitação.';
            mensagem.style.color = 'var(--error)';
        }
    } catch (error) {
        console.error(error);
        mensagem.textContent =
            'Erro de conexão com o servidor. Verifique se a API está rodando.';
        mensagem.style.color = 'var(--error)';
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Entrar na Fila';
    }
});
