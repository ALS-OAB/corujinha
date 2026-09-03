import json

resumo_md_path = '/home/sfy/Corujinha/ETICA/01_orgaos_da_oab_resumo.md'
questoes_json_path = '/home/sfy/Corujinha/ETICA/01_orgaos_da_oab_questoes.json'
out_html_path = '/home/sfy/Corujinha/ETICA/Etica_RetaFinal_Premium.html'

with open(resumo_md_path, 'r', encoding='utf-8') as f:
    resumo_text = f.read()

with open(questoes_json_path, 'r', encoding='utf-8') as f:
    questoes = json.load(f)

# Convert Markdown to HTML for the summary modal
def simple_md_to_html(md):
    import re
    html = md
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.M)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.M)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.M)
    html = re.sub(r'^\> (.*?)$', r'<blockquote>\1</blockquote>', html, flags=re.M)
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    
    lines = html.split('\n')
    out_lines = []
    in_list = False
    in_table = False
    
    for line in lines:
        if line.strip().startswith('|'):
            if not in_table:
                out_lines.append('<div style="overflow-x:auto;"><table style="width:100%; border-collapse:collapse; margin:15px 0; font-size:13px;">')
                in_table = True
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if '---' in cells[0]:
                continue
            tag = 'th' if '---' in line or (len(out_lines) > 0 and 'table' in out_lines[-1]) else 'td'
            cell_html = ''.join([f'<{tag} style="border:1px solid #cbd5e1; padding:8px 10px;">{c}</{tag}>' for c in cells])
            out_lines.append(f'<tr>{cell_html}</tr>')
        else:
            if in_table:
                out_lines.append('</table></div>')
                in_table = False
            
            if line.strip().startswith('* ') or line.strip().startswith('- '):
                if not in_list:
                    out_lines.append('<ul>')
                    in_list = True
                out_lines.append(f'<li>{line.strip()[2:]}</li>')
            else:
                if in_list:
                    out_lines.append('</ul>')
                    in_list = False
                if line.strip():
                    if not line.startswith('<h') and not line.startswith('<block'):
                        out_lines.append(f'<p>{line.strip()}</p>')
                else:
                    out_lines.append('<br>')
    if in_list: out_lines.append('</ul>')
    if in_table: out_lines.append('</table></div>')
    return '\n'.join(out_lines)

resumo_html = simple_md_to_html(resumo_text)

resumo_struct = [{
    'title': 'Módulo 1: Órgãos da OAB (Estatuto e Regulamento Geral)',
    'body': resumo_html
}]

questions_json_str = json.dumps(questoes, ensure_ascii=False)
resumos_json_str = json.dumps(resumo_struct, ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ética Profissional · Órgãos da OAB · Exame de Ordem 47</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #f8fafc;
  --card: #ffffff;
  --primary: #1e1b4b;
  --primary-accent: #312e81;
  --accent: #4f46e5;
  --accent-soft: rgba(79,70,229,0.08);
  --text: #334155;
  --text-dim: #64748b;
  --border: #e2e8f0;
  --shadow: 0 10px 25px -5px rgba(0,0,0,0.08);
  --blue: #1d4ed8;
  --blue-bg: #eff6ff;
  --amber: #b45309;
  --amber-bg: #fffbeb;
  --rose: #be123c;
  --rose-bg: #fff1f2;
  --green: #047857;
  --green-bg: #ecfdf5;
}}
* {{ margin:0; padding:0; box-sizing:border-box; -webkit-tap-highlight-color:transparent; }}
html, body {{ height:100%; font-family:'Inter', sans-serif; background:var(--bg); color:var(--text); overflow:hidden; }}

p {{ margin-bottom: 12px; line-height: 1.6; font-size: 14px; }}
p:last-child {{ margin-bottom: 0; }}
h1 {{ font-size: 24px; color: var(--primary); margin-bottom: 12px; }}
h2 {{ font-size: 18px; color: var(--primary); margin: 24px 0 12px 0; }}
h3 {{ font-size: 15px; color: var(--accent); margin: 20px 0 10px 0; display:flex; align-items:center; gap:6px; }}
ul {{ padding-left: 20px; margin-bottom: 16px; }}
li {{ margin-bottom: 8px; line-height: 1.5; font-size: 14px; }}
strong {{ font-weight: 700; color: #1e293b; }}
blockquote {{ background: var(--amber-bg); border-left: 4px solid var(--amber); padding: 12px 16px; margin: 16px 0; border-radius: 0 8px 8px 0; font-style: italic; color: #78350f; }}
hr {{ border: 0; border-top: 1px solid var(--border); margin: 24px 0; }}

.bg {{ position:fixed; inset:0; z-index:0;
  background: radial-gradient(at 0% 0%, rgba(79,70,229,0.05) 0, transparent 50%),
              radial-gradient(at 100% 100%, rgba(30,27,75,0.05) 0, transparent 50%); }}

.hd {{ position:fixed; top:0; left:0; right:0; z-index:200; height:64px;
  background:rgba(255,255,255,0.92); border-bottom:1px solid var(--border);
  display:flex; align-items:center; justify-content:space-between;
  padding:0 24px; backdrop-filter:blur(12px); }}
.hd-left {{ display:flex; align-items:center; gap:10px; }}
.hd-logo {{ background:var(--primary); color:#fff; font-weight:800; font-size:12px;
  padding:5px 10px; border-radius:6px; letter-spacing:.5px; }}
.hd-title {{ font-size:13px; font-weight:700; color:var(--primary); text-transform:uppercase; letter-spacing:0.5px; }}
.hd-right {{ display:flex; align-items:center; gap:10px; }}

.btn-resumo {{ padding:7px 16px; border-radius:6px; border:none;
  font-size:12px; font-weight:700; cursor:pointer; background:var(--accent);
  color:#fff; transition:all .2s; box-shadow: 0 2px 4px rgba(79,70,229,0.2); }}
.btn-resumo:hover {{ background:var(--primary-accent); }}

.counter-pill {{ font-size:12px; font-weight:700; color:var(--accent);
  background:var(--accent-soft); padding:5px 14px; border-radius:20px; }}

.main {{ position:fixed; inset:0; top:64px; bottom:72px; overflow:hidden; z-index:1; }}
.carousel {{ display:flex; height:100%; transition:transform .45s cubic-bezier(.4,0,.2,1); }}
.slide {{ min-width:100%; height:100%; display:flex; align-items:center; justify-content:center; padding:15px; }}

.intro-card {{ background:var(--card); border-radius:24px; padding:36px;
  box-shadow:var(--shadow); max-width:720px; width:100%; max-height:85vh; overflow-y:auto; border:1px solid var(--border); }}
.intro-card h1 {{ font-family:'Cormorant Garamond',serif; font-size:clamp(24px,4vw,36px);
  color:var(--primary); margin-bottom:12px; line-height:1.2; }}
.intro-card p {{ color:var(--text-dim); font-size:14px; margin-bottom:20px; line-height:1.6; }}
.intro-badge {{ display:inline-block; background:var(--accent-soft); color:var(--accent); font-weight:700; font-size:11px; padding:4px 10px; border-radius:12px; margin-bottom:16px; text-transform:uppercase; }}

.q-card {{ perspective:1200px; max-width:720px; width:100%; height:min(640px, calc(100vh - 150px)); cursor:pointer; }}
.q-inner {{ width:100%; height:100%; position:relative; transform-style:preserve-3d; transition:transform .7s cubic-bezier(.4,0,.2,1); }}
.q-inner.flipped {{ transform:rotateY(180deg); }}
.q-face {{ position:absolute; inset:0; backface-visibility:hidden; border-radius:24px;
  box-shadow:var(--shadow); overflow-y:auto; overflow-x:hidden; background:var(--card); border:1px solid var(--border); }}

.q-front {{ padding:20px 24px; display:flex; flex-direction:column; gap:10px; justify-content:space-between; }}
.q-back {{ padding:20px 24px; transform:rotateY(180deg); display:flex; flex-direction:column; gap:14px; }}

.q-meta {{ display:flex; align-items:center; gap:8px; flex-wrap:wrap; flex-shrink:0; }}
.q-num {{ font-size:12px; font-weight:700; color:var(--accent); background:var(--accent-soft);
  padding:4px 12px; border-radius:12px; }}
.q-tema {{ font-size:11px; color:var(--text-dim); font-weight:600; }}
.timer-bar-wrap {{ height:4px; background:#f1f5f9; border-radius:2px; overflow:hidden; flex-shrink:0; margin-top:2px; }}
.timer-bar {{ height:100%; background:var(--accent); border-radius:2px; transition:width 1s linear, background .3s; }}
.timer-count {{ font-size:11px; font-weight:700; color:var(--text-dim); text-align:right; flex-shrink:0; }}

.q-enunc {{ margin-bottom:4px; flex-shrink:0; }}
.q-enunc p {{ color:var(--primary); font-size:clamp(13px,2.2vw,14.5px); font-weight:500; line-height:1.45; }}

.options {{ display:flex; flex-direction:column; gap:8px; flex:1; justify-content:center; }}
.opt {{ display:flex; align-items:flex-start; gap:10px; padding:12px 14px; border-radius:12px;
  border:1.5px solid var(--border); cursor:pointer; transition:all .2s; font-size:13px; line-height:1.4; background:#fff; }}
.opt:hover {{ border-color:var(--accent); background:var(--accent-soft); }}
.opt.selected {{ border-color:var(--accent); background:var(--accent-soft); }}
.opt.correct {{ border-color:var(--green); background:var(--green-bg); color:#065f46; font-weight:600; }}
.opt.wrong {{ border-color:var(--rose); background:var(--rose-bg); color:#9f1239; }}
.opt-letter {{ font-weight:800; color:var(--accent); min-width:18px; font-size:13.5px; margin-top:1px; }}

.gab-badge {{ display:inline-flex; align-items:center; gap:8px; background:#d1fae5;
  color:#065f46; font-weight:800; font-size:14px; padding:10px 18px; border-radius:12px; flex-shrink:0; width:fit-content; }}
.back-section {{ background:var(--blue-bg); border-left:4px solid var(--blue);
  padding:14px 16px; border-radius:0 12px 12px 0; }}
.back-section.legal {{ background:var(--amber-bg); border-color:var(--amber); }}
.back-section.dica {{ background:var(--rose-bg); border-color:var(--rose); }}
.back-section.teacher {{ background: #f0fdf4; border-left: 4px solid #16a34a; }}
.back-section.logica {{ background: #fff7ed; border-left: 4px solid #ea580c; }}
.back-section.alternatives {{ background: #f5f3ff; border-color: #8b5cf6; }}
.back-section-title {{ font-size:11px; font-weight:800; text-transform:uppercase;
  letter-spacing:.5px; color:var(--blue); margin-bottom:6px; }}
.back-section.legal .back-section-title {{ color:var(--amber); }}
.back-section.dica .back-section-title {{ color:var(--rose); }}
.back-section.teacher .back-section-title {{ color: #15803d; }}
.back-section.logica .back-section-title {{ color: #c2410c; }}
.back-section.alternatives .back-section-title {{ color: #8b5cf6; }}

.flip-hint {{ font-size:11px; color:var(--text-dim); text-align:center; flex-shrink:0; padding-top:6px; border-top:1px dashed var(--border); font-weight:500; }}

.ft {{ position:fixed; bottom:0; left:0; right:0; z-index:200; height:72px;
  background:rgba(255,255,255,0.95); border-top:1px solid var(--border);
  display:flex; align-items:center; justify-content:space-between;
  padding:0 24px; backdrop-filter:blur(12px); gap:12px; }}
.nav-btn {{ padding:12px 24px; border-radius:8px; border:none; font-size:14px;
  font-weight:700; cursor:pointer; transition:all .2s; flex:1; max-width:160px; }}
.btn-prev {{ background:#e2e8f0; color:var(--text); }}
.btn-prev:hover {{ background:#cbd5e1; }}
.btn-next {{ background:var(--accent); color:#fff; }}
.btn-next:hover {{ background:var(--primary-accent); }}
.score-pill {{ font-size:13px; font-weight:800; color:var(--primary);
  background:var(--accent-soft); padding:8px 18px; border-radius:20px; white-space:nowrap; text-align:center; }}

.result-card {{ background:var(--card); border-radius:24px; padding:48px 36px;
  text-align:center; max-width:520px; width:100%; box-shadow:var(--shadow); border:1px solid var(--border); }}
.result-score {{ font-size:64px; font-weight:800; color:var(--primary); line-height:1; }}
.result-label {{ font-size:16px; color:var(--text-dim); margin-top:8px; margin-bottom:24px; }}
.result-pct {{ font-size:24px; font-weight:800; color:var(--accent); margin-bottom:32px; }}
.btn-restart {{ padding:14px 36px; background:var(--accent); color:#fff; border:none;
  border-radius:8px; font-size:15px; font-weight:700; cursor:pointer; transition:.2s; }}
.btn-restart:hover {{ background:var(--primary-accent); }}

.modal-overlay {{ position:fixed; inset:0; background:rgba(0,0,0,0.5); z-index:999; display:none; justify-content:center; align-items:center; backdrop-filter:blur(4px); }}
.modal-content {{ background:#fff; width:95%; max-width:760px; max-height:85vh; border-radius:20px; display:flex; flex-direction:column; overflow:hidden; box-shadow:0 25px 50px -12px rgba(0,0,0,0.25); }}
.modal-header {{ padding:18px 24px; border-bottom:1px solid var(--border); display:flex; justify-content:space-between; align-items:center; background:var(--blue-bg); }}
.modal-header h2 {{ font-size:18px; color:var(--blue); margin:0; }}
.btn-close {{ background:none; border:none; font-size:24px; cursor:pointer; color:var(--text-dim); }}
.modal-body {{ padding:0; overflow-y:auto; flex:1; display:flex; flex-direction:column; }}
.resumo-btn {{ padding:18px 24px; text-align:left; border:none; border-bottom:1px solid var(--border); background:#fff; font-size:15px; font-weight:700; color:var(--primary); cursor:pointer; transition:.2s; }}
.resumo-btn:hover {{ background:var(--bg); }}
.resumo-text {{ padding:24px; display:none; background:#fff; border-bottom:1px solid var(--border); }}
.resumo-text.active {{ display:block; }}

@media (max-width: 600px) {{
  .hd {{ padding:0 12px; }} 
  .ft {{ padding:0 12px; }}
  .q-front, .q-back {{ padding:18px 14px; }}
  .intro-card {{ padding:24px 18px; }}
  .hd-title {{ font-size: 11px; }} 
  .btn-resumo {{ padding: 6px 10px; font-size: 11px; }}
  .nav-btn {{ padding: 10px 14px; font-size: 13px; }}
}}
</style>
</head>
<body>
<div class="bg"></div>

<header class="hd">
  <div class="hd-left">
    <span class="hd-logo">OAB 47</span>
    <span class="hd-title">ÉTICA · ÓRGÃOS DA OAB</span>
  </div>
  <div class="hd-right">
    <button class="btn-resumo" onclick="openModal()">📚 Resumos</button>
    <span class="counter-pill" id="counter">1 / 15</span>
  </div>
</header>

<div class="modal-overlay" id="resumo-modal" onclick="closeModal(event)">
  <div class="modal-content" onclick="event.stopPropagation()">
    <div class="modal-header">
      <h2>📚 Resumo de Véspera · Órgãos da OAB</h2>
      <button class="btn-close" onclick="closeModal(event)">&times;</button>
    </div>
    <div class="modal-body" id="modal-body"></div>
  </div>
</div>

<main class="main">
  <div class="carousel" id="carousel"></div>
</main>

<footer class="ft">
  <button class="nav-btn btn-prev" onclick="navigate(-1)">← Voltar</button>
  <span class="score-pill" id="score">Acertos: 0</span>
  <button class="nav-btn btn-next" onclick="navigate(1)">Avançar →</button>
</footer>

<script>
const ALL_QUESTIONS = {questions_json_str};
const RESUMOS = {resumos_json_str};

let questions = [...ALL_QUESTIONS];
let currentIdx = 0;
let score = 0;
let answered = {{}};
let timerInterval = null;
let timerValue = 45;

function openModal() {{
  const m = document.getElementById('resumo-modal');
  const b = document.getElementById('modal-body');
  if (b.children.length === 0) {{
      RESUMOS.forEach((r, idx) => {{
        const btn = document.createElement('button');
        btn.className = 'resumo-btn';
        btn.innerHTML = `📖 ${{r.title}}`;
        
        const txt = document.createElement('div');
        txt.className = 'resumo-text';
        txt.id = `resumo-txt-${{idx}}`;
        txt.innerHTML = r.body;
        
        btn.onclick = () => {{
          const isActive = txt.classList.contains('active');
          document.querySelectorAll('.resumo-text').forEach(el => el.classList.remove('active'));
          if (!isActive) txt.classList.add('active');
        }};
        
        b.appendChild(btn);
        b.appendChild(txt);
      }});
  }}
  m.style.display = 'flex';
}}

function closeModal(e) {{
  if(e) e.preventDefault();
  document.getElementById('resumo-modal').style.display = 'none';
}}

function buildCarousel() {{
  const c = document.getElementById('carousel');
  c.innerHTML = '';

  const intro = document.createElement('div');
  intro.className = 'slide';
  intro.innerHTML = `
    <div class="intro-card">
      <span class="intro-badge">Reta Final OAB 47 · Módulo 1</span>
      <h1>Órgãos da OAB: Estrutura, Personalidade & Competências</h1>
      <p>Material de revisão ativa baseado na aula especial da <strong>Profª. Maria Christina (Gran Cursos OAB)</strong>. Contém <strong>15 questões comentadas</strong> com foco nos temas mais recorrentes da banca FGV.</p>
      <p>💡 <strong>Como estudar:</strong> Clique no botão <strong>"📚 Resumos"</strong> no topo para revisar a teoria rápida antes das questões. Toque na alternativa desejada para testar seu conhecimento e virar o card automaticamente!</p>
      <button class="btn-restart" style="margin-top:10px;" onclick="navigate(1)">🚀 Iniciar Simulado (15 Questões)</button>
    </div>`;
  c.appendChild(intro);

  questions.forEach((q, i) => {{
    const slide = document.createElement('div');
    slide.className = 'slide';
    slide.innerHTML = buildQuestionSlide(q, i);
    c.appendChild(slide);
  }});

  const result = document.createElement('div');
  result.className = 'slide';
  result.id = 'result-slide';
  result.innerHTML = `
    <div class="result-card">
      <div class="result-score" id="final-score">0</div>
      <div class="result-label">acertos de <strong>${{questions.length}}</strong> questões de Órgãos da OAB</div>
      <div class="result-pct" id="final-pct">0%</div>
      <button class="btn-restart" onclick="location.reload()">🔄 Refazer Simulado</button>
    </div>`;
  c.appendChild(result);
  updateCounter();
}}

function buildQuestionSlide(q, i) {{
  const optsHtml = Object.entries(q.opcoes).map(([k,v]) => `
    <div class="opt" id="opt-${{i}}-${{k}}" onclick="selectOpt(${{i}}, '${{k}}')">
      <span class="opt-letter">${{k}}</span>
      <span>${{v}}</span>
    </div>`).join('');

  return `
    <div class="q-card" id="qcard-${{i}}">
      <div class="q-inner" id="qinner-${{i}}">
        <div class="q-face q-front">
          <div class="q-meta">
            <span class="q-num">Q${{i+1}} / ${{questions.length}}</span>
            <span class="q-tema">${{q.tema}}</span>
          </div>
          <div class="timer-bar-wrap"><div class="timer-bar" id="tbar-${{i}}"></div></div>
          <div class="timer-count" id="tcount-${{i}}">45s</div>
          <div class="q-enunc">${{q.enunciado}}</div>
          <div class="options">${{optsHtml}}</div>
          <div class="flip-hint">Toque em uma resposta para verificar e virar o card</div>
        </div>
        <div class="q-face q-back" onclick="unflip(${{i}})">
          <span class="gab-badge">✅ Gabarito: ${{q.gabarito}})</span>
          ${{q.aula_comentario ? '<div class="back-section teacher"><div class="back-section-title">🎙️ Explicação da Professora na Aula</div>' + q.aula_comentario + '</div>' : ''}}
          ${{q.logica_conceito ? '<div class="back-section logica"><div class="back-section-title">💡 Entendendo a Lógica do Conceito (Por que é assim?)</div>' + q.logica_conceito + '</div>' : ''}}
          <div class="back-section">
            <div class="back-section-title">📚 Síntese Teórica</div>
            ${{q.sintese}}
          </div>
          <div class="back-section legal">
            <div class="back-section-title">⚖️ Fundamentação Jurídica</div>
            ${{q.fundamentacao}}
          </div>
          <div class="back-section dica">
            <div class="back-section-title">🚨 Dica de Prova</div>
            ${{q.dica}}
          </div>
          ${{q.analise ? '<div class="back-section alternatives"><div class="back-section-title">🔍 Análise das Alternativas</div>' + q.analise + '</div>' : ''}}
          <div class="flip-hint">Toque no card para voltar à pergunta</div>
        </div>
      </div>
    </div>`;
}}

function selectOpt(i, letter) {{
  if (answered[i] !== undefined) return;
  answered[i] = letter;
  const q = questions[i];
  const isCorrect = letter === q.gabarito;
  if (isCorrect) score++;
  document.getElementById('score').textContent = `Acertos: ${{score}}`;

  ['A','B','C','D'].forEach(k => {{
    const el = document.getElementById(`opt-${{i}}-${{k}}`);
    if (!el) return;
    if (k === q.gabarito) el.classList.add('correct');
    else if (k === letter && !isCorrect) el.classList.add('wrong');
  }});

  stopTimer();
  setTimeout(() => flipCard(i), 850);
}}

function flipCard(i) {{
  document.getElementById(`qinner-${{i}}`).classList.add('flipped');
}}
function unflip(i) {{
  document.getElementById(`qinner-${{i}}`).classList.remove('flipped');
}}

function startTimer(i) {{
  stopTimer();
  timerValue = 45;
  const bar = document.getElementById(`tbar-${{i}}`);
  const cnt = document.getElementById(`tcount-${{i}}`);
  if (!bar || !cnt) return;
  bar.style.width = '100%';
  bar.style.background = 'var(--accent)';
  timerInterval = setInterval(() => {{
    timerValue--;
    const pct = (timerValue / 45) * 100;
    bar.style.width = pct + '%';
    cnt.textContent = timerValue + 's';
    if (timerValue <= 10) {{ bar.style.background = '#ef4444'; cnt.style.color = '#ef4444'; }}
    if (timerValue <= 0) {{
      stopTimer();
      if (answered[i] === undefined) flipCard(i);
    }}
  }}, 1000);
}}
function stopTimer() {{
  clearInterval(timerInterval);
  timerInterval = null;
}}

function goTo(idx) {{
  const total = questions.length + 2;
  currentIdx = Math.max(0, Math.min(idx, total - 1));
  const c = document.getElementById('carousel');
  c.style.transform = `translateX(-${{currentIdx * 100}}%)`;
  stopTimer();
  if (currentIdx > 0 && currentIdx <= questions.length) {{
    const qIdx = currentIdx - 1;
    if (answered[qIdx] === undefined) startTimer(qIdx);
  }}
  if (currentIdx === questions.length + 1) {{
    document.getElementById('final-score').textContent = score;
    document.getElementById('final-pct').textContent = Math.round((score / questions.length) * 100) + '%';
  }}
  updateCounter();
}}

function navigate(dir) {{ goTo(currentIdx + dir); }}

function updateCounter() {{
  const total = questions.length;
  let label;
  if (currentIdx === 0) label = `Início`;
  else if (currentIdx > total) label = `Fim`;
  else label = `${{currentIdx}} / ${{total}}`;
  document.getElementById('counter').textContent = label;
}}

buildCarousel();
goTo(0);
</script>
</body>
</html>
'''

with open(out_html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Etica_RetaFinal_Premium.html gerado com sucesso!')
