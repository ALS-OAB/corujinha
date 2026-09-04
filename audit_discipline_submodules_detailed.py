import os
import json
import glob

CORUJINHA_DIR = '/home/sfy/Corujinha'
folders = [d for d in os.listdir(CORUJINHA_DIR) if os.path.isdir(os.path.join(CORUJINHA_DIR, d)) and d not in ['assets', '.git', '__pycache__']]
folders.sort()

print(f"=== DIAGNÓSTICO DETALHADO POR MÓDULO (20 DISCIPLINAS) ===\n")

total_ecosystem_questions = 0
discipline_summary = []

for folder in folders:
    folder_path = os.path.join(CORUJINHA_DIR, folder)
    json_files = sorted(glob.glob(os.path.join(folder_path, '*_questoes.json')))
    
    disc_total_q = 0
    modules_info = []
    
    for jf in json_files:
        filename = os.path.basename(jf)
        with open(jf, 'r', encoding='utf-8') as f:
            qs = json.load(f)
        count = len(qs)
        disc_total_q += count
        
        # Check completeness of questions
        incomplete_count = 0
        for q in qs:
            if not q.get('enunciado') or not q.get('gabarito') or not q.get('opcoes'):
                incomplete_count += 1
                
        modules_info.append({
            'file': filename,
            'count': count,
            'incomplete': incomplete_count
        })
        
    total_ecosystem_questions += disc_total_q
    discipline_summary.append({
        'folder': folder,
        'total_questions': disc_total_q,
        'modules_count': len(json_files),
        'modules': modules_info
    })
    
    print(f"📌 DISCIPLINAS: {folder:<22} | Total: {disc_total_q:3d} q | Módulos: {len(json_files):2d}")
    for m in modules_info:
        inc_mark = f" ⚠️ ({m['incomplete']} incompletas)" if m['incomplete'] > 0 else ""
        print(f"   ├─ {m['file']:<35}: {m['count']:2d} questões{inc_mark}")
    print()

print(f"=========================================================")
print(f"TOTAL DE QUESTÕES EM TODO O ECOSSISTEMA CORUJINHA: {total_ecosystem_questions}")
print(f"=========================================================")
