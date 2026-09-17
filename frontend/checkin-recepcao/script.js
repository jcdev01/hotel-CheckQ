const API_URL = 'http://127.0.0.1:8000';

async function carregarFila() {
    try {
        const response = await fetch(`${API_URL}/fila`);
        const fila = await response.json();
        atualizarInterface(fila);
    } catch (error) {
        console.error('Erro ao buscar a fila:', error);
        mostrarToast('Erro de conexão com a API');
    }
}

function atualizarInterface(fila) {
    const counterNumber = document.getElementById('counterNumber');
    const checkinContent = document.getElementById('checkinContent');
    const emptyState = document.getElementById('emptyState');
    const upcomingList = document.getElementById('upcomingList');

    counterNumber.textContent = fila.length;
    
    // sequencia para a fila vazia ou com alguém e para mostrar ao lado
    if (fila.length === 0) {
        checkinContent.hidden = true;
        emptyState.hidden = false;
        upcomingList.innerHTML = '<p>Nenhum hóspede aguardando.</p>';
        return;
    }

    checkinContent.hidden = false;
    emptyState.hidden = true;

    const atual = fila[0];
    document.getElementById('guestName').textContent = atual.nome_hospede;
    document.getElementById('guestRoom').textContent = `Quarto ${atual.numero_quarto}`;
    
    const dataEntrada = new Date(atual.horario_entrada);
    document.getElementById('guestCheckin').textContent = dataEntrada.toLocaleString('pt-BR');
    
    const dataSaida = new Date(atual.horario_saida);
    document.getElementById('guestCheckout').textContent = dataSaida.toLocaleString('pt-BR');
    
    document.getElementById('guestAvatar').textContent = atual.nome_hospede.charAt(0).toUpperCase();
    document.getElementById('guestPosition').textContent = '1º da fila';

    upcomingList.innerHTML = '';
    for (let i = 1; i < fila.length; i++) {
        const hospede = fila[i];
        const item = document.createElement('div');
        item.style.padding = '10px 0';
        item.style.borderBottom = '1px solid #ccc';
        item.innerHTML = `<strong>${i + 1}º</strong> - ${hospede.nome_hospede} (Quarto ${hospede.numero_quarto})`;
        upcomingList.appendChild(item);
    }
}

// Botão de registrar check-in e sequencia para atender o proximo da fila
document.getElementById('attendBtn').addEventListener('click', async () => {
    try {
        const response = await fetch(`${API_URL}/fila/proximo`, {
            method: 'DELETE'
        });

        if (response.ok) {
            mostrarToast('Check-in concluído com sucesso!');
            carregarFila();
        } else {
            mostrarToast('Erro ao atender hóspede.');
        }
    } catch (error) {
        console.error(error);
        mostrarToast('Erro de conexão.');
    }
});

function mostrarToast(mensagem) {
    const toast = document.getElementById('toast');
    toast.textContent = mensagem;
    toast.style.display = 'block';
    setTimeout(() => { toast.style.display = 'none'; }, 3000);
}

carregarFila();
setInterval(carregarFila, 5000);