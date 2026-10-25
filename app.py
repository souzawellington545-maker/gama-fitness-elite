import os
import sqlite3
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)
DB_NAME = "gama_elite_final.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            academia_id TEXT DEFAULT 'Gama Fitness',
            nome TEXT NOT NULL,
            telefone TEXT DEFAULT '',
            idade INTEGER NOT NULL,
            objetivo TEXT NOT NULL,
            plano TEXT DEFAULT 'Plano Mensal',
            mensalidade REAL NOT NULL,
            status_pagamento TEXT DEFAULT 'Pendente',
            forma_pagamento TEXT DEFAULT 'Pendente',
            vencimento TEXT DEFAULT 'Dia 10'
        )
    ''')
    conn.commit()
    conn.close()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Gama Fitness | Gestão Elite</title>
    <style>
        :root {
            --bg-deep: #030303;
            --card-bg: #0e0e0e;
            --card-border: #222222;
            --gold: #facc15;
            --gold-glow: rgba(250, 204, 21, 0.2);
            --gold-hover: #eab308;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --whatsapp: #25d366;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        * { box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background: var(--bg-deep); margin: 0; padding: 14px; color: var(--text-main); }
        .app-container { max-width: 650px; margin: auto; }
        
        header { 
            text-align: center; 
            margin-bottom: 18px; 
            padding: 22px 15px; 
            background: linear-gradient(145deg, #121212, #080808); 
            border: 1px solid var(--card-border); 
            border-radius: 18px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
            position: relative;
        }
        header::after {
            content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
            background: linear-gradient(90deg, transparent, var(--gold), transparent);
        }

        .header-content { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
        
        .gold-dumbbell-box {
            background: rgba(250, 204, 21, 0.1);
            border: 1px solid rgba(250, 204, 21, 0.3);
            width: 50px;
            height: 50px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--gold);
            box-shadow: 0 0 12px var(--gold-glow);
            flex-shrink: 0;
        }
        .gold-dumbbell-box svg { width: 28px; height: 28px; fill: currentColor; }

        .header-center { text-align: center; flex: 1; }
        .brand-title { font-size: 24px; font-weight: 900; color: var(--gold); letter-spacing: 1.5px; margin: 0; text-transform: uppercase; text-shadow: 0 2px 10px rgba(250,204,21,0.2); }
        .brand-subtitle { color: var(--text-muted); font-size: 10px; text-transform: uppercase; letter-spacing: 3px; margin-top: 5px; font-weight: 700; }

        .metrics-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 18px; }
        .metric-card { 
            background: var(--card-bg); 
            border: 1px solid var(--card-border); 
            padding: 14px 8px; 
            border-radius: 14px; 
            text-align: center;
        }
        .metric-card span { display: block; font-size: 9px; color: var(--text-muted); text-transform: uppercase; font-weight: 800; margin-bottom: 4px; }
        .metric-card strong { font-size: 18px; font-weight: 800; }

        .panel-card { 
            background: var(--card-bg); 
            border: 1px solid var(--card-border); 
            padding: 20px; 
            margin-bottom: 18px; 
            border-radius: 16px;
        }
        h3 { margin: 0 0 16px 0; color: var(--gold); font-size: 15px; border-bottom: 1px solid var(--card-border); padding-bottom: 10px; font-weight: 800; display: flex; justify-content: space-between; align-items: center; }

        .form-group { margin-bottom: 12px; }
        input, select { 
            width: 100%; 
            padding: 13px; 
            background: #050505; 
            border: 1px solid var(--card-border); 
            color: var(--text-main); 
            border-radius: 10px; 
            font-size: 13px;
        }
        input:focus, select:focus { border-color: var(--gold); outline: none; box-shadow: 0 0 0 3px var(--gold-glow); }
        
        button.btn-main { 
            background: var(--gold); 
            color: #000; 
            border: none; 
            padding: 15px; 
            width: 100%; 
            border-radius: 10px; 
            font-size: 14px; 
            cursor: pointer; 
            font-weight: 900; 
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        button.btn-main:hover { background: var(--gold-hover); }

        .filter-tabs { display: flex; gap: 6px; margin-bottom: 14px; }
        .tab-btn { 
            flex: 1; 
            background: #050505; 
            border: 1px solid var(--card-border); 
            color: var(--text-muted); 
            padding: 9px 0; 
            border-radius: 8px; 
            font-size: 10px; 
            font-weight: 800; 
            cursor: pointer; 
            text-transform: uppercase;
            text-align: center;
        }
        .tab-btn.active { background: var(--gold); color: #000; border-color: var(--gold); }

        .client-item { 
            background: #050505; 
            border: 1px solid var(--card-border); 
            border-left: 4px solid var(--gold); 
            padding: 15px; 
            margin-top: 10px; 
            border-radius: 12px;
        }
        .client-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
        .client-name { font-weight: 800; font-size: 15px; color: var(--text-main); }
        
        .badge { font-size: 9px; padding: 4px 8px; border-radius: 20px; font-weight: 900; text-transform: uppercase; }
        .badge.pago { background: rgba(16, 185, 129, 0.15); color: var(--success); border: 1px solid rgba(16, 185, 129, 0.3); }
        .badge.pendente { background: rgba(245, 158, 11, 0.15); color: var(--warning); border: 1px solid rgba(245, 158, 11, 0.3); }

        .client-info { font-size: 12px; color: var(--text-muted); margin-bottom: 10px; line-height: 1.6; }
        
        .payment-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin-bottom: 10px; }
        .btn-pay { 
            background: #141414; 
            border: 1px solid var(--card-border); 
            color: #fff; 
            padding: 8px 2px; 
            border-radius: 8px; 
            font-size: 10px; 
            font-weight: 800; 
            cursor: pointer; 
            text-align: center;
        }
        .btn-pay:hover { border-color: var(--gold); color: var(--gold); }

        .action-row { display: flex; gap: 8px; align-items: center; }
        
        .btn-icon-wsp {
            background: rgba(37, 211, 102, 0.15);
            border: 1px solid rgba(37, 211, 102, 0.4);
            color: var(--whatsapp);
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            flex-shrink: 0;
        }
        .btn-icon-wsp:hover { background: var(--whatsapp); color: #000; }
        .btn-icon-wsp svg { width: 20px; height: 20px; fill: currentColor; }

        .btn-undo {
            background: rgba(245, 158, 11, 0.12);
            border: 1px solid rgba(245, 158, 11, 0.3);
            color: var(--warning);
            padding: 0 10px;
            height: 40px;
            border-radius: 10px;
            font-size: 10px;
            font-weight: 800;
            cursor: pointer;
            text-transform: uppercase;
        }

        .btn-delete {
            background: rgba(239, 68, 68, 0.12);
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: var(--danger);
            padding: 0 10px;
            height: 40px;
            border-radius: 10px;
            font-size: 10px;
            font-weight: 800;
            cursor: pointer;
            flex: 1;
            text-transform: uppercase;
        }

        .empty-state { text-align: center; color: var(--text-muted); padding: 20px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="app-container">
        <header>
            <div class="header-content">
                <div class="gold-dumbbell-box" title="Treino de Elite">
                    <svg viewBox="0 0 24 24"><path d="M20.57 14.86L22 13.43 20.57 12 17 15.57 8.43 7 12 3.43 10.57 2 9.14 3.43 7.71 2 6.29 3.43 4.86 2 3.43 3.43 4.86 4.86 2 7.71l1.43 1.43L2 10.57 3.43 12 7 8.43 15.57 17 12 20.57 13.43 22l1.43-1.43L16.29 22l1.42-1.43 1.43 1.43 1.43-1.43-1.43-1.43L20.57 14.86z"/></svg>
                </div>
                
                <div class="header-center">
                    <div class="brand-title">Gama Fitness ⚡</div>
                    <div class="brand-subtitle">Força • Foco • Evolução</div>
                </div>

                <div class="gold-dumbbell-box" title="Treino de Elite">
                    <svg viewBox="0 0 24 24"><path d="M20.57 14.86L22 13.43 20.57 12 17 15.57 8.43 7 12 3.43 10.57 2 9.14 3.43 7.71 2 6.29 3.43 4.86 2 3.43 3.43 4.86 4.86 2 7.71l1.43 1.43L2 10.57 3.43 12 7 8.43 15.57 17 12 20.57 13.43 22l1.43-1.43L16.29 22l1.42-1.43 1.43 1.43 1.43-1.43-1.43-1.43L20.57 14.86z"/></svg>
                </div>
            </div>
        </header>

        <div class="metrics-grid">
            <div class="metric-card">
                <span>Alunos</span>
                <strong id="m-total">0</strong>
            </div>
            <div class="metric-card">
                <span>Caixa Pago</span>
                <strong id="m-pago" style="color: var(--success);">R$ 0</strong>
            </div>
            <div class="metric-card">
                <span>A Receber</span>
                <strong id="m-pend" style="color: var(--warning);">R$ 0</strong>
            </div>
        </div>

        <div class="panel-card">
            <h3>Cadastrar Novo Aluno</h3>
            <div class="form-group">
                <input type="text" id="academia_id" placeholder="Unidade / Nome da Academia" value="Gama Fitness">
            </div>
            <div class="form-group"><input type="text" id="nome" placeholder="Nome Completo do Aluno"></div>
            <div class="form-group"><input type="text" id="telefone" placeholder="WhatsApp (DDD + Número)"></div>
            
            <div style="display:flex; gap:8px;" class="form-group">
                <input type="number" id="idade" placeholder="Idade" style="flex:1;">
                <select id="plano" style="flex:1.2;">
                    <option value="Plano Mensal" selected>Mensal</option>
                    <option value="Trimestral">Trimestral</option>
                    <option value="Semestral">Semestral</option>
                    <option value="Anual">Anual</option>
                </select>
                <select id="vencimento" style="flex:1;">
                    <option value="Dia 05">Dia 05</option>
                    <option value="Dia 10" selected>Dia 10</option>
                    <option value="Dia 15">Dia 15</option>
                    <option value="Dia 20">Dia 20</option>
                </select>
            </div>
            
            <div class="form-group"><input type="text" id="objetivo" placeholder="Objetivo (Ex: Musculação / Performance)"></div>
            <div class="form-group"><input type="number" id="mensalidade" placeholder="Valor da Mensalidade (R$)"></div>
            <button class="btn-main" onclick="cadastrarAluno()">Cadastrar Aluno</button>
        </div>

        <div class="panel-card">
            <h3>Gestão & Cobrança</h3>
            
            <div class="filter-tabs">
                <button class="tab-btn active" onclick="setFiltro('todos', this)">Todos</button>
                <button class="tab-btn" onclick="setFiltro('pago', this)">Em Dia</button>
                <button class="tab-btn" onclick="setFiltro('pendente', this)">Inadimplentes</button>
            </div>

            <div class="form-group">
                <input type="text" id="busca" placeholder="🔍 Buscar por nome..." oninput="carregarAlunos()">
            </div>
            <div id="lista-alunos"><div class="empty-state">A carregar registos...</div></div>
        </div>
    </div>

    <script>
        let filtroStatus = 'todos';

        function setFiltro(status, btn) {
            filtroStatus = status;
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            carregarAlunos();
        }

        async function carregarAlunos() {
            let res = await fetch('/api/alunos');
            let alunos = await res.json();
            let busca = document.getElementById('busca').value.toLowerCase();

            let total = alunos.length;
            let pago = 0, pend = 0;

            alunos.forEach(a => {
                let v = parseFloat(a.mensalidade) || 0;
                if(a.status_pagamento === 'Pago') pago += v;
                else pend += v;
            });

            document.getElementById('m-total').innerText = total;
            document.getElementById('m-pago').innerText = `R$ ${pago.toFixed(0)}`;
            document.getElementById('m-pend').innerText = `R$ ${pend.toFixed(0)}`;

            let filtrados = alunos.filter(a => {
                let matchNome = a.nome.toLowerCase().includes(busca);
                if(filtroStatus === 'pago') return matchNome && a.status_pagamento === 'Pago';
                if(filtroStatus === 'pendente') return matchNome && a.status_pagamento === 'Pendente';
                return matchNome;
            });

            let html = '';
            if(filtrados.length === 0) {
                html = '<div class="empty-state">Nenhum registo encontrado.</div>';
            } else {
                filtrados.forEach(a => {
                    let v = parseFloat(a.mensalidade) || 0;
                    let num = a.telefone ? a.telefone.replace(/\D/g, '') : '';
                    
                    let wspMsg = '';
                    if(a.status_pagamento === 'Pago') {
                        wspMsg = encodeURIComponent(`Olá ${a.nome}! Passando para confirmar que recebemos o pagamento da sua mensalidade na Gama Fitness (${a.plano} - R$ ${v.toFixed(2)}). Muito obrigado e ótimo treino! ⚡💪`);
                    } else {
                        wspMsg = encodeURIComponent(`Olá ${a.nome}! Lembramos que a sua mensalidade da Gama Fitness (${a.plano} - R$ ${v.toFixed(2)}) está pendente. Podemos gerar o código Pix?`);
                    }
                    
                    let wspLink = num ? `https://wa.me/55${num}?text=${wspMsg}` : '#';

                    let svgWsp = `<svg viewBox="0 0 24 24"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>`;

                    html += `<div class="client-item">
                        <div class="client-header">
                            <span class="client-name">${a.nome}</span>
                            <span class="badge ${a.status_pagamento === 'Pago' ? 'pago' : 'pendente'}">${a.status_pagamento}</span>
                        </div>
                        <div class="client-info">
                            Unidade: <b>${a.academia_id}</b> | Plano: <b>${a.plano}</b><br>
                            Vencimento: <b>${a.vencimento}</b> | Objetivo: <b>${a.objetivo}</b><br>
                            Valor: <b>R$ ${v.toFixed(2)}</b> | Método: <b style="color:var(--gold);">${a.forma_pagamento}</b>
                        </div>
                        
                        <div style="font-size:9px; color:var(--text-muted); margin-bottom:4px; font-weight:800;">DAR BAIXA VIA:</div>
                        <div class="payment-grid">
                            <button class="btn-pay" onclick="darBaixa(${a.id}, 'Pix')">⚡ Pix</button>
                            <button class="btn-pay" onclick="darBaixa(${a.id}, 'Cartão')">💳 Cartão</button>
                            <button class="btn-pay" onclick="darBaixa(${a.id}, 'Boleto')">📄 Boleto</button>
                            <button class="btn-pay" onclick="darBaixa(${a.id}, 'Dinheiro')">💵 Dinheiro</button>
                        </div>

                        <div class="action-row">
                            ${num ? `<a href="${wspLink}" target="_blank" class="btn-icon-wsp" title="WhatsApp">${svgWsp}</a>` : ''}
                            ${a.status_pagamento === 'Pago' ? `<button class="btn-undo" onclick="estornar(${a.id})">↩️ Estornar</button>` : ''}
                            <button class="btn-delete" onclick="remover(${a.id})">Excluir</button>
                        </div>
                    </div>`;
                });
            }
            document.getElementById('lista-alunos').innerHTML = html;
        }

        async function cadastrarAluno() {
            let academia_id = document.getElementById('academia_id').value.trim() || 'Gama Fitness';
            let nome = document.getElementById('nome').value.trim();
            let telefone = document.getElementById('telefone').value.trim();
            let idade = document.getElementById('idade').value;
            let plano = document.getElementById('plano').value;
            let vencimento = document.getElementById('vencimento').value;
            let objetivo = document.getElementById('objetivo').value.trim() || 'Performance';
            let mensalidade = document.getElementById('mensalidade').value;

            if(!nome || !idade) return alert('Preencha os campos obrigatórios (Nome e Idade)!');

            await fetch('/api/alunos', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({academia_id, nome, telefone, idade, plano, vencimento, objetivo, mensalidade})
            });

            document.getElementById('nome').value = '';
            document.getElementById('telefone').value = '';
            document.getElementById('idade').value = '';
            document.getElementById('objetivo').value = '';
            document.getElementById('mensalidade').value = '';
            carregarAlunos();
        }

        async function darBaixa(id, metodo) {
            await fetch(`/api/alunos/${id}/pagamento`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({forma_pagamento: metodo, status: 'Pago'})
            });
            carregarAlunos();
        }

        async function estornar(id) {
            await fetch(`/api/alunos/${id}/pagamento`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({forma_pagamento: 'Pendente', status: 'Pendente'})
            });
            carregarAlunos();
        }

        async function remover(id) {
            if(confirm('Deseja realmente remover este registo?')) {
                await fetch(`/api/alunos/${id}`, {method: 'DELETE'});
                carregarAlunos();
            }
        }

        carregarAlunos();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/alunos', methods=['GET'])
def listar():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, academia_id, nome, telefone, idade, objetivo, plano, mensalidade, status_pagamento, forma_pagamento, vencimento FROM alunos')
    rows = c.fetchall()
    conn.close()
    return jsonify([{
        "id": r[0], "academia_id": r[1], "nome": r[2], "telefone": r[3],
        "idade": r[4], "objetivo": r[5], "plano": r[6], "mensalidade": r[7],
        "status_pagamento": r[8], "forma_pagamento": r[9], "vencimento": r[10]
    } for r in rows])

@app.route('/api/alunos', methods=['POST'])
def criar():
    d = request.get_json()
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO alunos (academia_id, nome, telefone, idade, objetivo, plano, mensalidade, status_pagamento, forma_pagamento, vencimento)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Pendente', 'Pendente', ?)
    ''', (d.get('academia_id','Gama Fitness'), d.get('nome'), d.get('telefone',''), d.get('idade'), d.get('objetivo','Performance'), d.get('plano','Plano Mensal'), d.get('mensalidade',0), d.get('vencimento','Dia 10')))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

@app.route('/api/alunos/<int:aluno_id>/pagamento', methods=['PUT'])
def pagamento(aluno_id):
    d = request.get_json()
    status = d.get('status', 'Pago')
    forma = d.get('forma_pagamento', 'Pix')
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE alunos SET status_pagamento = ?, forma_pagamento = ? WHERE id = ?", (status, forma, aluno_id))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

@app.route('/api/alunos/<int:aluno_id>', methods=['DELETE'])
def deletar(aluno_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM alunos WHERE id = ?', (aluno_id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
