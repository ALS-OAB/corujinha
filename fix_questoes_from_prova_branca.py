"""
fix_questoes_from_prova_branca.py
==================================
Corrige enunciados e alternativas dos JSONs do Corujinha
usando a prova tipo 1 (branca) original como única fonte da verdade.

Uso:
    python3 fix_questoes_from_prova_branca.py              # todas as disciplinas
    python3 fix_questoes_from_prova_branca.py ETICA        # só Ética
    python3 fix_questoes_from_prova_branca.py ETICA CPC    # múltiplas

Suporta:
  - Separadores de questão com 1 a 6 # (#{1,6} N)
  - 3 formatos de alternativas: A) / - A) / - (A)
  - Limpeza de lixo de rodapé/cabeçalho de página
  - Correção de DOC_Documentos → documentos (artefato da conversão PDF→MD)
"""
import re, json, glob, os, sys

BASE_PROVA   = '/home/sfy/Jurimetria_OAB/QST_Questoes'
BASE_CORPUS  = '/home/sfy/Corujinha'

# Separador de questão: mínimo 4 # seguido de número isolado
# Seções de página usam 1-3 #; questões usam ####, ##### ou ######
QUESTAO_SEP = re.compile(r'#{4,6}\s+(\d+)\s*\n')

# Padrões de lixo de rodapé/cabeçalho
LIXO = [
    re.compile(r'^\d+$'),                               # número de página isolado
    re.compile(r'^[IVXLCDM]+\s+EXAME DE ORDEM', re.I), # 'XXXVII EXAME DE ORDEM UN'
    re.compile(r'PROVA APLICADA', re.I),
    re.compile(r'NIFICADO\s*[–\-]\s*TIPO', re.I),       # 'UNIFICADO – TIPO 1 – BRANCA'
    re.compile(r'^A EM \d{1,2}/\d{1,2}/\d{4}$'),       # 'A EM 26/2/2023'
    re.compile(r'QUESTIONÁRIO DE PERCEPÇÃO', re.I),
    re.compile(r'^#{1,6}\s*$'),                         # linha só com # (residual)
]

ALT_PATTERN = re.compile(
    r'(?:^|\n)- \(([ABCD])\)(.*?)(?=\n- \([ABCD]\)|\Z)'   # - (A)
    r'|(?:^|\n)- ([ABCD])\)(.*?)(?=\n- [ABCD]\)|\Z)'       # - A)
    r'|(?:^|\n)([ABCD])\)(.*?)(?=\n[ABCD]\)|\Z)',          # A)
    re.DOTALL
)
FIRST_ALT = re.compile(r'\n(?:- \([ABCD]\)|(?:- )?[ABCD]\))')


def parse_questao(num, texto):
    texto = clean_lixo(texto).strip()
    m = FIRST_ALT.search(texto)
    if not m:
        return {'num': num, 'enunciado': texto, 'alternativas': {}}
    enunciado = texto[:m.start()].strip()
    resto = texto[m.start():]
    alternativas = {}
    for match in ALT_PATTERN.finditer(resto):
        letra = match.group(1) or match.group(3) or match.group(5)
        conteudo = match.group(2) or match.group(4) or match.group(6)
        if letra:
            alternativas[letra] = clean_lixo(conteudo).strip()
    return {'num': num, 'enunciado': enunciado, 'alternativas': alternativas}


def clean_lixo(texto):
    """Remove rodapés/cabeçalhos de página e artefatos de conversão PDF→MD."""
    # Corrigir DOC_Documentos → documentos (artefato do conversor PDF→MD)
    texto = texto.replace('DOC_Documentos', 'documentos')
    linhas = texto.split('\n')
    return '\n'.join(l for l in linhas if not any(p.search(l.strip()) for p in LIXO if l.strip()))


def parse_md_questoes(caminho_md):
    """Extrai questões 1-80 do MD da prova branca (para antes do questionário de percepção).
    Suporta separadores com 1 a 6 # (#{1,6} N) conforme o conversor usado em cada exame."""
    content = open(caminho_md).read()
    parts = QUESTAO_SEP.split(content)
    questoes = {}
    ultimo_num = 0
    for i in range(1, len(parts), 2):
        num = int(parts[i])
        if num < ultimo_num:   # regressão = início do questionário de percepção
            break
        ultimo_num = num
        texto = parts[i+1] if i+1 < len(parts) else ''
        questoes[num] = parse_questao(num, texto)
    return questoes


_md_cache = {}
def get_md(exame_num):
    if exame_num not in _md_cache:
        path = f'{BASE_PROVA}/exame_{exame_num}/primeira_fase/prova_tipo1_branca.md'
        if not os.path.exists(path):
            _md_cache[exame_num] = {}
        else:
            _md_cache[exame_num] = parse_md_questoes(path)
    return _md_cache[exame_num]


def auditar_alternativas(dados, modulo):
    """Verifica completude das 4 alternativas em cada questão."""
    problemas = []
    for q in dados:
        alts = q.get('alternativas', {})
        for letra in ['A', 'B', 'C', 'D']:
            v = alts.get(letra, '')
            if not v:
                problemas.append(f'  VAZIA  : {modulo} Q{q["num"]}E{q["exame_num"]} alt {letra}')
            elif len(v) < 8:
                problemas.append(f'  CURTA  : {modulo} Q{q["num"]}E{q["exame_num"]} alt {letra}: {repr(v)}')
    return problemas


def processar_disciplina(disciplina):
    jsons = sorted(glob.glob(f'{BASE_CORPUS}/{disciplina}/*_questoes.json'))
    if not jsons:
        print(f'  {disciplina}: nenhum JSON encontrado')
        return 0, 0, 0

    total_ok = total_falha = total_problemas = 0
    auditoria = []

    for jpath in jsons:
        dados = json.load(open(jpath))
        falhas = []
        for q in dados:
            exame_num = q.get('exame_num')
            num = q.get('num')
            md = get_md(exame_num)
            md_q = md.get(num)
            if not md_q:
                falhas.append(f'Q{num}E{exame_num}')
                total_falha += 1
                continue
            q['enunciado'] = md_q['enunciado']
            q['alternativas'] = md_q['alternativas']
            total_ok += 1

        modulo = os.path.basename(jpath).replace('_questoes.json', '')
        auditoria += auditar_alternativas(dados, modulo)

        json.dump(dados, open(jpath, 'w'), ensure_ascii=False, indent=2)
        status = f'{len(dados)} questões'
        if falhas:
            status += f' | FALHAS: {falhas}'
        print(f'  {os.path.basename(jpath)}: {status}')

    total_problemas = len(auditoria)
    if auditoria:
        print(f'\n  *** PROBLEMAS DE ALTERNATIVA ({total_problemas}):')
        for p in auditoria:
            print(p)
    else:
        print(f'  Auditoria: todas as alternativas OK')

    return total_ok, total_falha, total_problemas


# Mapear diretórios de disciplinas
DISCIPLINAS = [
    d for d in sorted(os.listdir(BASE_CORPUS))
    if os.path.isdir(f'{BASE_CORPUS}/{d}')
    and glob.glob(f'{BASE_CORPUS}/{d}/*_questoes.json')
    and d not in ('assets',)
]

# Filtrar por argumento de linha de comando, se houver
alvos = sys.argv[1:] if len(sys.argv) > 1 else DISCIPLINAS
invalidos = [a for a in alvos if a not in DISCIPLINAS]
if invalidos:
    print(f'Disciplinas não encontradas: {invalidos}')
    print(f'Disponíveis: {DISCIPLINAS}')
    sys.exit(1)

print(f'Disciplinas encontradas: {DISCIPLINAS}\n')

grand_ok = grand_falha = grand_prob = 0
for disc in alvos:
    print(f'\n=== {disc} ===')
    ok, falha, prob = processar_disciplina(disc)
    grand_ok += ok
    grand_falha += falha
    grand_prob += prob

print(f'\n{"="*50}')
print(f'TOTAL: {grand_ok} questões corrigidas | {grand_falha} não encontradas | {grand_prob} alternativas com problema')
