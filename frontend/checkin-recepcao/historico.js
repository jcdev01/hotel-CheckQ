const API_URL = 'http://127.0.0.1:8000';

async function carregarHistorico() {
    const container = document.getElementById('historicoContainer');
    
    try {
        const response = await fetch(`${API_URL}/historico`);
        const historico = await response.json();

        if (historico.length === 0) {
            container.innerHTML = '<p style="color: var(--text-muted);">Nenhum check-in registrado no histórico ainda.</p>';
            return;
        }

        let html = `
            <table class="historico-table">
                <thead>
                    <tr>
                        <th>Hóspede</th>
                        <th>Quarto</th>
                        <th>Entrada</th>
                        <th>Saída</th>
                    </tr>
                </thead>
                <tbody>
        `;

        historico.forEach(item => {
            const dataEntrada = new Date(item.horario_entrada).toLocaleString('pt-BR');
            const dataSaida = new Date(item.horario_saida).toLocaleString('pt-BR');
            
            html += `
                <tr>
                    <td style="font-weight: 500;">${item.nome_hospede}</td>
                    <td>${item.numero_quarto}</td>
                    <td>${dataEntrada}</td>
                    <td>${dataSaida}</td>
                </tr>
            `;
        });

        html += `</tbody></table>`;
        container.innerHTML = html;

    } catch (error) {
        console.error('Erro ao buscar histórico:', error);
        container.innerHTML = '<p style="color: red;">Erro ao conectar com a API para carregar o histórico.</p>';
    }
}

carregarHistorico();