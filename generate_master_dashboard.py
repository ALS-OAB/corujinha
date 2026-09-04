import os
import json
import glob

CORUJINHA_DIR = '/home/sfy/Corujinha'

disciplines = [
    {"code": "ETICA", "name": "Ética Profissional", "icon": "⚖️", "weight": "12 quest/exame", "color": "#f59e0b", "questions": 122, "dashboard": "ETICA/Dashboard_Etica_Premium.html"},
    {"code": "CIVIL", "name": "Direito Civil", "icon": "📜", "weight": "6 quest/exame", "color": "#3b82f6", "questions": 56, "dashboard": "CIVIL/Dashboard_Civil_Premium.html"},
    {"code": "CPC", "name": "Processo Civil", "icon": "🏛️", "weight": "6 quest/exame", "color": "#6366f1", "questions": 60, "dashboard": "CPC/Dashboard_CPC_Premium.html"},
    {"code": "PENAL", "name": "Direito Penal", "icon": "🛡️", "weight": "6 quest/exame", "color": "#ef4444", "questions": 59, "dashboard": "PENAL/Dashboard_Penal_Premium.html"},
    {"code": "PROCESSUAL_PENAL", "name": "Processo Penal", "icon": "🔒", "weight": "6 quest/exame", "color": "#dc2626", "questions": 57, "dashboard": "PROCESSUAL_PENAL/Dashboard_ProcessualPenal_Premium.html"},
    {"code": "CONSTITUCIONAL", "name": "Direito Constitucional", "icon": "🇧🇷", "weight": "6 quest/exame", "color": "#10b981", "questions": 59, "dashboard": "CONSTITUCIONAL/Dashboard_Constitucional_Premium.html"},
    {"code": "ADMINISTRATIVO", "name": "Direito Administrativo", "icon": "🏙️", "weight": "5 quest/exame", "color": "#14b8a6", "questions": 50, "dashboard": "ADMINISTRATIVO/Dashboard_Administrativo_Premium.html"},
    {"code": "TRIBUTARIO", "name": "Direito Tributário", "icon": "💰", "weight": "5 quest/exame", "color": "#8b5cf6", "questions": 50, "dashboard": "TRIBUTARIO/Dashboard_Tributario_Premium.html"},
    {"code": "TRABALHISTA", "name": "Direito do Trabalho", "icon": "💼", "weight": "5 quest/exame", "color": "#ec4899", "questions": 49, "dashboard": "TRABALHISTA/Dashboard_Trabalhista_Premium.html"},
    {"code": "PROCESSUAL_TRABALHISTA", "name": "Processo do Trabalho", "icon": "📑", "weight": "5 quest/exame", "color": "#f43f5e", "questions": 49, "dashboard": "PROCESSUAL_TRABALHISTA/Dashboard_ProcessualTrabalhista_Premium.html"},
    {"code": "EMPRESARIAL", "name": "Direito Empresarial", "icon": "🏢", "weight": "4 quest/exame", "color": "#0284c7", "questions": 40, "dashboard": "EMPRESARIAL/Dashboard_Empresarial_Premium.html"},
    {"code": "FILOSOFIA", "name": "Filosofia do Direito", "icon": "🧠", "weight": "2 quest/exame", "color": "#a855f7", "questions": 21, "dashboard": "FILOSOFIA/Dashboard_Filosofia_Premium.html"},
    {"code": "AMBIENTAL", "name": "Direito Ambiental", "icon": "🌿", "weight": "2 quest/exame", "color": "#22c55e", "questions": 21, "dashboard": "AMBIENTAL/Dashboard_Ambiental_Premium.html"},
    {"code": "DIREITOS_HUMANOS", "name": "Direitos Humanos", "icon": "🌐", "weight": "2 quest/exame", "color": "#06b6d4", "questions": 20, "dashboard": "DIREITOS_HUMANOS/Dashboard_DireitosHumanos_Premium.html"},
    {"code": "INTERNACIONAL", "name": "Direito Internacional", "icon": "✈️", "weight": "2 quest/exame", "color": "#38bdf8", "questions": 20, "dashboard": "INTERNACIONAL/Dashboard_Internacional_Premium.html"},
    {"code": "ECA", "name": "Direito da Criança e Adolescente (ECA)", "icon": "👶", "weight": "2 quest/exame", "color": "#fbbf24", "questions": 19, "dashboard": "ECA/Dashboard_ECA_Premium.html"},
    {"code": "CONSUMIDOR", "name": "Direito do Consumidor", "icon": "🛒", "weight": "2 quest/exame", "color": "#f97316", "questions": 18, "dashboard": "CONSUMIDOR/Dashboard_Consumidor_Premium.html"},
    {"code": "ELEITORAL", "name": "Direito Eleitoral", "icon": "🗳️", "weight": "2 quest/exame", "color": "#84cc16", "questions": 18, "dashboard": "ELEITORAL/Dashboard_Eleitoral_Premium.html"},
    {"code": "PREVIDENCIARIO", "name": "Direito Previdenciário", "icon": "👴", "weight": "2 quest/exame", "color": "#eab308", "questions": 18, "dashboard": "PREVIDENCIARIO/Dashboard_Previdenciario_Premium.html"},
    {"code": "FINANCEIRO", "name": "Direito Financeiro", "icon": "📊", "weight": "2 quest/exame", "color": "#64748b", "questions": 18, "dashboard": "FINANCEIRO/Dashboard_Financeiro_Premium.html"}
]

# Generate Master Dashboard HTML
html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Plataforma Corujinha OAB · Portal Principal</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #0f172a;
      --card-bg: rgba(30, 41, 59, 0.7);
      --card-border: rgba(255, 255, 255, 0.1);
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --accent: #38bdf8;
      --accent-glow: rgba(56, 189, 248, 0.25);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    body {{
      background: radial-gradient(circle at top center, #1e1b4b 0%, #0f172a 60%, #020617 100%);
      color: var(--text);
      min-height: 100vh;
      padding: 30px 20px;
    }}

    .container {{
      max-width: 1300px;
      margin: 0 auto;
    }}

    header {{
      text-align: center;
      margin-bottom: 40px;
    }}

    .brand-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(99, 102, 241, 0.15);
      border: 1px solid rgba(129, 140, 248, 0.3);
      padding: 6px 16px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 700;
      color: #818cf8;
      margin-bottom: 16px;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }}

    h1 {{
      font-size: 42px;
      font-weight: 800;
      background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 12px;
    }}

    p.subtitle {{
      color: var(--text-muted);
      font-size: 17px;
      max-width: 700px;
      margin: 0 auto 30px;
      line-height: 1.6;
    }}

    .stats-bar {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 40px;
    }}

    .stat-card {{
      background: var(--card-bg);
      backdrop-filter: blur(12px);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 20px;
      text-align: center;
    }}

    .stat-val {{
      font-size: 32px;
      font-weight: 800;
      color: var(--accent);
    }}

    .stat-lbl {{
      font-size: 13px;
      color: var(--text-muted);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .search-box {{
      margin-bottom: 30px;
      position: relative;
    }}

    .search-box input {{
      width: 100%;
      padding: 16px 24px;
      border-radius: 14px;
      background: rgba(30, 41, 59, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #fff;
      font-size: 16px;
      outline: none;
      transition: all 0.2s;
    }}

    .search-box input:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 20px var(--accent-glow);
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 20px;
    }}

    .disc-card {{
      background: var(--card-bg);
      backdrop-filter: blur(12px);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 24px;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      text-decoration: none;
      color: inherit;
      position: relative;
      overflow: hidden;
    }}

    .disc-card:hover {{
      transform: translateY(-5px);
      border-color: rgba(255, 255, 255, 0.3);
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
    }}

    .disc-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
    }}

    .disc-icon {{
      font-size: 36px;
      background: rgba(255, 255, 255, 0.05);
      width: 56px;
      height: 56px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 14px;
    }}

    .disc-badge {{
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.1);
      color: var(--text-muted);
    }}

    .disc-title {{
      font-size: 20px;
      font-weight: 700;
      margin-bottom: 8px;
    }}

    .disc-meta {{
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 16px;
      padding-top: 16px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
    }}

    .btn-open {{
      margin-top: 16px;
      width: 100%;
      padding: 12px;
      border-radius: 10px;
      background: linear-gradient(135deg, #3b82f6, #1d4ed8);
      color: #fff;
      font-weight: 700;
      text-align: center;
      font-size: 14px;
      border: none;
      cursor: pointer;
      transition: opacity 0.2s;
    }}

    .disc-card:hover .btn-open {{
      opacity: 0.9;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="brand-badge">🦉 Plataforma Corujinha OAB · Portal Central</div>
      <h1>Central de Simulados & Módulos OAB</h1>
      <p class="subtitle">Acesse todos os 20 ecossistemas de disciplinas, com 824 questões oficiais auditadas (Exames 37 ao 46) e didática completa.</p>
    </header>

    <div class="stats-bar">
      <div class="stat-card">
        <div class="stat-val">20</div>
        <div class="stat-lbl">Disciplinas Auditadas</div>
      </div>
      <div class="stat-card">
        <div class="stat-val">824</div>
        <div class="stat-lbl">Questões Oficiais FGV</div>
      </div>
      <div class="stat-card">
        <div class="stat-val">160</div>
        <div class="stat-lbl">Módulos Interativos</div>
      </div>
      <div class="stat-card">
        <div class="stat-val">100%</div>
        <div class="stat-lbl">Gabarito & Didática</div>
      </div>
    </div>

    <div class="search-box">
      <input type="text" id="searchInput" placeholder="Pesquisar disciplina (ex: Civil, Ética, Penal, Constitucional...)" onkeyup="filterDisciplines()">
    </div>

    <div class="grid" id="discGrid">
"""

for d in disciplines:
    html_content += f"""
      <a class="disc-card" href="{d['dashboard']}" data-name="{d['name'].lower()}">
        <div>
          <div class="disc-header">
            <div class="disc-icon">{d['icon']}</div>
            <div class="disc-badge" style="color:{d['color']}">{d['weight']}</div>
          </div>
          <div class="disc-title">{d['name']}</div>
        </div>
        <div>
          <div class="disc-meta">
            <span>{d['questions']} Questões Auditadas</span>
            <span>Exames 37–46</span>
          </div>
          <div class="btn-open" style="background: {d['color']};">Abrir Dashboard →</div>
        </div>
      </a>
"""

html_content += """
    </div>
  </div>

  <script>
    function filterDisciplines() {
      const q = document.getElementById('searchInput').value.toLowerCase();
      const cards = document.querySelectorAll('.disc-card');
      cards.forEach(c => {
        const name = c.getAttribute('data-name');
        if (name.includes(q)) {
          c.style.display = 'flex';
        } else {
          c.style.display = 'none';
        }
      });
    }
  </script>
</body>
</html>
"""

with open(os.path.join(CORUJINHA_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_content)

print("🎉 Master Portal Dashboard criado com sucesso em /home/sfy/Corujinha/index.html!")
