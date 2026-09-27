const API_URL = 'http://127.0.0.1:8000';

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('identificacao').value.trim();
    const senha = document.getElementById('senha').value;
    const btn = document.getElementById('submitBtn');

    if (!email || !senha) {
        Swal.fire({
            icon: 'warning',
            title: 'Campos obrigatórios',
            text: 'Preencha o e-mail e a senha.',
            confirmButtonText: 'OK'
        });
        return;
    }

    btn.disabled = true;
    btn.textContent = 'Autenticando...';

    // Alerta de carregamento
    Swal.fire({
        title: 'Entrando...',
        text: 'Verificando suas credenciais.',
        allowOutsideClick: false,
        allowEscapeKey: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

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

            await Swal.fire({
                icon: 'success',
                title: 'Login realizado!',
                text: `Bem-vindo, ${dados.nome}!`,
                confirmButtonText: 'Continuar',
                timer: 2000,
                timerProgressBar: true
            });

            window.location.href = '../checkin-app/index.html';

        } else {

            Swal.fire({
                icon: 'error',
                title: 'Falha no login',
                text: dados.detail || 'E-mail ou senha incorretos.',
                confirmButtonText: 'Tentar novamente'
            });
        }

    } catch (error) {

        console.error('Erro no login:', error);

        Swal.fire({
            icon: 'error',
            title: 'Erro de conexão',
            text: 'Não foi possível conectar ao servidor da API.',
            confirmButtonText: 'OK'
        });

    } finally {
        btn.disabled = false;
        btn.textContent = 'Entrar no Sistema';
    }
});