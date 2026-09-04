import os
import json
import glob
from collections import defaultdict, Counter

SIMULADOS_DIR = '/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados'
files = sorted(glob.glob(os.path.join(SIMULADOS_DIR, 'e*_tipo1_branca.json')))

print(f"=== FASE 1: VARREDURA E MAPEAMENTO DIAGNÓSTICO DO CADERNO MESTRE ===")
print(f"Encontrados {len(files)} exames da OAB (Exames 37 ao 46).\n")

all_master_questions = []
discipline_counts = defaultdict(Counter)
gabarito_distribution = Counter()
invalid_questions = []

for fpath in files:
    filename = os.path.basename(fpath)
    exame_num = int(filename.split('e')[1].split('_')[0])
    exame_label = f"{exame_num}º Exame OAB"
    
    with open(fpath, 'r', encoding='utf-8') as f:
        items = json.load(f)
        
    print(f"📄 {exame_label}: {len(items)} questões lidas.")
    
    for item in items:
        num = item.get('num', 0)
        disc = item.get('disciplina', 'Sem Disciplina')
        gabarito = str(item.get('gabarito', '')).upper().strip()
        opcoes = item.get('opcoes', [])
        enunciado = item.get('enunciado', '')
        
        # Validation checks
        if not gabarito or gabarito not in ['A', 'B', 'C', 'D']:
            invalid_questions.append((exame_label, num, f"Gabarito inválido: '{gabarito}'"))
        if len(opcoes) != 4:
            invalid_questions.append((exame_label, num, f"Qtd de opções incorreta: {len(opcoes)}"))
        if not enunciado:
            invalid_questions.append((exame_label, num, "Enunciado vazio"))
            
        discipline_counts[disc][exame_label] += 1
        gabarito_distribution[gabarito] += 1
        
        item['exame_num'] = exame_num
        item['exame_label'] = exame_label
        all_master_questions.append(item)

print(f"\n✅ Total de questões mapeadas no acervo mestre: {len(all_master_questions)}")

if invalid_questions:
    print(f"⚠️ ATENÇÃO: Encontradas {len(invalid_questions)} inconformidades no gabarito/opções:")
    for inv in invalid_questions:
        print(f"   - {inv[0]} Q{inv[1]}: {inv[2]}")
else:
    print("✨ 100% das 800 questões possuem gabarito válido (A, B, C, D), 4 opções de resposta e enunciado completo.")

print("\n--- DISTRIBUIÇÃO DAS QUESTÕES POR DISCIPLINA (EXAMES 37 AO 46) ---")
table_header = f"{'Disciplina':<40} | " + " | ".join([f"E{i}" for i in range(37, 47)]) + " | Total"
print("-" * len(table_header))
print(table_header)
print("-" * len(table_header))

sorted_disciplines = sorted(discipline_counts.keys())
total_by_exam = defaultdict(int)

for disc in sorted_disciplines:
    counts_str = []
    disc_total = 0
    for ex in range(37, 47):
        c = discipline_counts[disc][f"{ex}º Exame OAB"]
        counts_str.append(f"{c:2d}")
        disc_total += c
        total_by_exam[ex] += c
    print(f"{disc:<40} | " + " | ".join(counts_str) + f" | {disc_total:5d}")

print("-" * len(table_header))
totals_str = " | ".join([f"{total_by_exam[ex]:2d}" for ex in range(37, 47)])
print(f"{'TOTAL GERAL POR EXAME':<40} | " + totals_str + f" | {len(all_master_questions):5d}")
print("-" * len(table_header))

print("\n--- DISTRIBUIÇÃO DE ALTERNATIVAS DO GABARITO DEFINITIVO ---")
for k, v in sorted(gabarito_distribution.items()):
    pct = (v / len(all_master_questions)) * 100
    print(f"  Alternativa {k}: {v:3d} questões ({pct:.1f}%)")

# Save master diagnostic JSON
with open('/home/sfy/Corujinha/master_diagnostico_oab.json', 'w', encoding='utf-8') as f:
    json.dump({
        'total_questions': len(all_master_questions),
        'disciplines': {d: dict(c) for d, c in discipline_counts.items()},
        'gabaritos': dict(gabarito_distribution)
    }, f, ensure_ascii=False, indent=2)

print("\n💾 Arquivo 'master_diagnostico_oab.json' salvo com sucesso!")
