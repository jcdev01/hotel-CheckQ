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

logoutBtn.addEventListener('click', (e) => {
    e.preventDefault();

    setTimeout(() => {
        Swal.fire({
            title: 'Sair da conta?',
            text: 'Você precisará fazer login novamente.',
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'Sim, sair',
            cancelButtonText: 'Cancelar',
            confirmButtonColor: '#d33'
        }).then((result) => {
            if (result.isConfirmed) {
                localStorage.removeItem('hospede_logado');
                window.location.href = '../login-app/index.html';
            }
        });
    }, 0);
});

checkinForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    submitBtn.disabled = true;
    submitBtn.textContent = 'Enviando...';
    mensagem.textContent = '';

    Swal.fire({
        title: 'Enviando solicitação...',
        allowOutsideClick: false,
        allowEscapeKey: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

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
    Swal.fire({
        title: 'Sucesso!',
        text: 'Check-in solicitado com sucesso! Aguarde na recepção.',
        icon: 'success',
        confirmButtonText: 'OK'
    });
    checkinForm.reset();
} else if (response.status === 409) {
    Swal.fire({
        title: 'Quarto ocupado',
        text: 'Este quarto já está ocupado!',
        icon: 'error',
        confirmButtonText: 'Entendi'
    });
} else if (response.status === 400) {
    const erroData = await response.json();
    Swal.fire({
        title: 'Dados inválidos',
        text: erroData.detail || 'Verifique os dados informados.',
        icon: 'warning',
        confirmButtonText: 'Entendi'
    });
} else {
    Swal.fire({
        title: 'Erro',
        text: 'Erro ao processar solicitação.',
        icon: 'error',
        confirmButtonText: 'Entendi'
    });
}
    } catch (error) {
        console.error(error);
        Swal.fire({
            title: 'Erro de conexão',
            text: 'Erro de conexão com o servidor. Verifique se a API está rodando.',
            icon: 'error',
            confirmButtonText: 'Entendi'
        });
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Entrar na Fila';
    }
});