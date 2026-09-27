const API_URL = 'http://127.0.0.1:8000';

document.getElementById('adminLoginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const usuario = document.getElementById('usuario').value.trim();
    const senha = document.getElementById('senha').value;
    const btn = document.getElementById('submitBtn');

    btn.disabled = true;
    btn.textContent = 'Autenticando...';

    // SweetAlert de carregamento
    Swal.fire({
        title: 'Autenticando...',
        text: 'Verificando suas credenciais.',
        allowOutsideClick: false,
        allowEscapeKey: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    try {
        const response = await fetch(`${API_URL}/admin/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: usuario,
                password: senha
            })
        });

        if (response.ok) {

            // SweetAlert de sucesso
            await Swal.fire({
                icon: 'success',
                title: 'Login realizado!',
                text: 'Acesso à recepção autorizado.',
                confirmButtonText: 'Continuar',
                timer: 2000,
                timerProgressBar: true
            });

            localStorage.setItem('admin_logado', 'true');

            window.location.href =
                '../checkin-recepcao/checkin_recepcao.html';

        } else {

            let mensagemErro = 'Usuário ou senha incorretos.';

            try {
                const dados = await response.json();

                if (dados.detail) {
                    mensagemErro = dados.detail;
                }
            } catch {
                // Mantém a mensagem padrão caso a API não retorne JSON
            }

            // SweetAlert de erro de autenticação
            await Swal.fire({
                icon: 'error',
                title: 'Falha no login',
                text: mensagemErro,
                confirmButtonText: 'Tentar novamente'
            });
        }

    } catch (error) {

        console.error('Erro no login:', error);

        // SweetAlert de erro de conexão
        await Swal.fire({
            icon: 'error',
            title: 'Erro de conexão',
            text: 'Não foi possível conectar ao servidor da API.',
            confirmButtonText: 'OK'
        });

    } finally {
        btn.disabled = false;
        btn.textContent = 'Entrar';
    }
});

