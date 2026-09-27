
const API_URL = 'http://127.0.0.1:8000';

document.getElementById('cadastroForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const btn = document.getElementById('submitBtn');

    btn.disabled = true;
    btn.textContent = 'Cadastrando...';

    const payload = {
        nome: document.getElementById('nome').value.trim(),
        cpf: document.getElementById('cpf').value.trim(),
        email: document.getElementById('email').value.trim(),
        telefone: document.getElementById('telefone').value.trim(),
        data_nascimento:
            document.getElementById('data_nascimento').value + 'T00:00:00',
        senha: document.getElementById('senha').value
    };

    // SweetAlert de carregamento
    Swal.fire({
        title: 'Criando sua conta...',
        text: 'Aguarde enquanto seus dados são cadastrados.',
        allowOutsideClick: false,
        allowEscapeKey: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    try {
        const response = await fetch(`${API_URL}/usuarios`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {

            await Swal.fire({
                icon: 'success',
                title: 'Cadastro realizado!',
                text: 'Sua conta foi criada com sucesso.',
                confirmButtonText: 'Ir para o login'
            });

            // Redireciona para o login
            window.location.href = 'login.html';

        } else {

            let mensagemErro = 'Erro ao realizar cadastro.';

            try {
                const erro = await response.json();

                if (erro.detail) {
                    mensagemErro = erro.detail;
                }
            } catch {
                // Mantém a mensagem padrão
            }

            await Swal.fire({
                icon: 'error',
                title: 'Não foi possível cadastrar',
                text: mensagemErro,
                confirmButtonText: 'Tentar novamente'
            });
        }

    } catch (error) {

        console.error('Erro no cadastro:', error);

        await Swal.fire({
            icon: 'error',
            title: 'Erro de conexão',
            text: 'Não foi possível conectar ao servidor da API.',
            confirmButtonText: 'OK'
        });

    } finally {
        btn.disabled = false;
        btn.textContent = 'Criar Conta';
    }
});

