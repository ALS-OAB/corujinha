"""
auditar_gabaritos.py
=====================
Cruza o campo 'gabarito' dos JSONs do Corujinha com o gabarito
definitivo da prova tipo 1 (branca) oficial.

Uso:
    python3 auditar_gabaritos.py              # todas as disciplinas
    python3 auditar_gabaritos.py ETICA        # só Ética
"""
import re, json, glob, os, sys

BASE_PROVA  = '/home/sfy/Jurimetria_OAB/QST_Questoes'
BASE_CORPUS = '/home/sfy/Corujinha'


def parse_gabarito_tipo1(caminho_md):
    """
    Extrai gabarito tipo 1 (branco) do MD do gabarito definitivo.
    Retorna dict {num_questao: letra} onde letra pode ser '*' (anulada).

    O gabarito TIPO 1 é sempre o primeiro bloco do arquivo.
    Para para quando encontra numeração que reinicia (início de outro tipo).
    """
    content = open(caminho_md).read()

    # Localizar início: primeira ocorrência de "TIPO 1" ou "PROVA 1" no arquivo
    m = re.search(r'(?:TIPO|PROVA)\s*1\b', content, re.I)
    if not m:
        return {}

    gabarito = {}
    ultimos_nums = []
    ultimo_max = 0  # último número máximo visto (para detectar reinício)

    for linha in content[m.start():].split('\n'):
        if not linha.strip() or '---' in linha:
            continue
        vals = [v.strip() for v in linha.strip('|').split('|') if v.strip()]
        if not vals:
            continue
        try:
            nums = [int(v) for v in vals]
            # Detectar reinício (novo tipo de prova: números começam de 1 novamente)
            if nums[0] <= ultimo_max and nums[0] == 1 and len(gabarito) >= 20:
                break
            ultimos_nums = nums
            ultimo_max = max(nums)
        except ValueError:
            # Linha de respostas: só aceitar letras OAB válidas
            resps = [v for v in vals if re.match(r'^[ABCD\*]$', v)]
            if ultimos_nums and len(resps) == len(ultimos_nums):
                for num, resp in zip(ultimos_nums, resps):
                    gabarito[num] = resp
                ultimos_nums = []
            elif vals and not re.match(r'^[A-Z\s\-º°\.]+$', vals[0]):
                # Linha estranha — ignorar silenciosamente
                pass

    return gabarito


_gab_cache = {}
def get_gabarito(exame_num):
    if exame_num not in _gab_cache:
        path = f'{BASE_PROVA}/exame_{exame_num}/primeira_fase/gabarito_definitivo.md'
        if not os.path.exists(path):
            _gab_cache[exame_num] = {}
        else:
            _gab_cache[exame_num] = parse_gabarito_tipo1(path)
    return _gab_cache[exame_num]


def auditar_disciplina(disciplina):
    jsons = sorted(glob.glob(f'{BASE_CORPUS}/{disciplina}/*_questoes.json'))
    if not jsons:
        return 0, 0, 0, 0

    total = corretos = divergentes = anuladas = sem_gab = 0
    divergencias = []

    for jpath in jsons:
        dados = json.load(open(jpath))
        modulo = os.path.basename(jpath).replace('_questoes.json', '')

        for q in dados:
            total += 1
            exame_num = q.get('exame_num')
            num = q.get('num')
            gab_json = (q.get('gabarito') or '').strip().upper()
            gab_oficial = get_gabarito(exame_num).get(num)

            if gab_oficial is None:
                sem_gab += 1
                divergencias.append(f'  SEM_GAB  : {modulo} Q{num}E{exame_num} — gabarito oficial não encontrado')
            elif gab_oficial == '*':
                anuladas += 1
                if gab_json not in ('*', 'ANULADA', ''):
                    divergencias.append(f'  ANULADA  : {modulo} Q{num}E{exame_num} — oficial=ANULADA, json={repr(gab_json)}')
            elif gab_json == gab_oficial:
                corretos += 1
            else:
                divergentes += 1
                divergencias.append(
                    f'  DIVERGE  : {modulo} Q{num}E{exame_num} — oficial={gab_oficial}, json={repr(gab_json)}'
                )

    return total, corretos, divergentes, anuladas, sem_gab, divergencias


# Disciplinas disponíveis
DISCIPLINAS = [
    d for d in sorted(os.listdir(BASE_CORPUS))
    if os.path.isdir(f'{BASE_CORPUS}/{d}')
    and glob.glob(f'{BASE_CORPUS}/{d}/*_questoes.json')
    and d not in ('assets',)
]

alvos = sys.argv[1:] if len(sys.argv) > 1 else DISCIPLINAS
invalidos = [a for a in alvos if a not in DISCIPLINAS]
if invalidos:
    print(f'Disciplinas não encontradas: {invalidos}')
    sys.exit(1)

grand_total = grand_ok = grand_div = grand_anu = grand_sem = 0
todas_diverg = []

for disc in alvos:
    total, ok, div, anu, sem, diverg = auditar_disciplina(disc)
    grand_total += total
    grand_ok    += ok
    grand_div   += div
    grand_anu   += anu
    grand_sem   += sem
    todas_diverg += diverg

    status = f'{ok}/{total} corretos'
    if div:  status += f', {div} DIVERGENTES'
    if anu:  status += f', {anu} anuladas'
    if sem:  status += f', {sem} sem gabarito oficial'
    print(f'{disc}: {status}')

print(f'\n{"="*55}')
print(f'TOTAL: {grand_ok}/{grand_total} corretos | {grand_div} divergentes | {grand_anu} anuladas | {grand_sem} sem gabarito')

if todas_diverg:
    print('\nDETALHE:')
    for d in todas_diverg:
        print(d)
else:
    print('\nNenhuma divergência encontrada.')
