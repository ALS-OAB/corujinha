import os
import json
import glob
from collections import defaultdict

CORUJINHA_DIR = '/home/sfy/Corujinha'
SIMULADOS_DIR = '/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados'

# 1. Load official master answer key registry
master_answer_key = {}
for sf in sorted(glob.glob(os.path.join(SIMULADOS_DIR, 'e*_tipo1_branca.json'))):
    exame_num = int(os.path.basename(sf).split('e')[1].split('_')[0])
    with open(sf, 'r', encoding='utf-8') as f:
        items = json.load(f)
    for item in items:
        num = item.get('num')
        disc = item.get('disciplina', '')
        gabarito = str(item.get('gabarito', '')).upper().strip()
        enunc_snippet = item.get('enunciado', '')[:60].strip()
        
        # Store by key
        key = (exame_num, num)
        master_answer_key[key] = {
            'exame': f"{exame_num}º Exame OAB",
            'num': num,
            'disciplina_oficial': disc,
            'gabarito_oficial': gabarito,
            'snippet': enunc_snippet
        }

print(f"✅ Mapeadas {len(master_answer_key)} questões no registro oficial de gabarito mestre.\n")

# 2. Audit all discipline folders in Corujinha
discipline_folders = [d for d in os.listdir(CORUJINHA_DIR) if os.path.isdir(os.path.join(CORUJINHA_DIR, d)) and d not in ['assets', '.git', '__pycache__']]
discipline_folders.sort()

print(f"=== AUDITORIA GERAL DE PASTAS DIDÁTICAS ({len(discipline_folders)} DISCIPLINAS) ===\n")

folder_audit_results = {}

for folder in discipline_folders:
    folder_path = os.path.join(CORUJINHA_DIR, folder)
    json_files = sorted(glob.glob(os.path.join(folder_path, '*_questoes.json')))
    
    total_questions = 0
    mismatched_discipline = []
    mismatched_gabarito = []
    missing_gabarito = 0
    
    for jf in json_files:
        with open(jf, 'r', encoding='utf-8') as f:
            qs = json.load(f)
        total_questions += len(qs)
        
        for q in qs:
            exame_num = q.get('exame_num')
            num = q.get('num')
            gabarito = str(q.get('gabarito', '')).upper().strip()
            
            # Check against master answer key
            key = (exame_num, num)
            if key in master_answer_key:
                master_info = master_answer_key[key]
                off_disc = master_info['disciplina_oficial']
                off_gab = master_info['gabarito_oficial']
                
                # Check discipline mismatch
                if off_disc and off_disc != folder and folder not in off_disc and off_disc not in folder:
                    mismatched_discipline.append({
                        'file': os.path.basename(jf),
                        'exame': f"{exame_num}º",
                        'num': num,
                        'disc_oficial': off_disc,
                        'pasta_atual': folder,
                        'snippet': q.get('enunciado', '')[:60]
                    })
                    
                # Check gabarito mismatch
                if gabarito and off_gab and gabarito != off_gab:
                    mismatched_gabarito.append({
                        'file': os.path.basename(jf),
                        'exame': f"{exame_num}º",
                        'num': num,
                        'gab_arquivo': gabarito,
                        'gab_oficial': off_gab
                    })
            else:
                missing_gabarito += 1
                
    folder_audit_results[folder] = {
        'total_json_files': len(json_files),
        'total_questions': total_questions,
        'disc_mismatches': len(mismatched_discipline),
        'gab_mismatches': len(mismatched_gabarito),
        'mismatched_discipline_details': mismatched_discipline,
        'mismatched_gabarito_details': mismatched_gabarito
    }
    
    status_icon = "✅ OK" if len(mismatched_discipline) == 0 and len(mismatched_gabarito) == 0 else "⚠️ AJUSTES NECESSÁRIOS"
    print(f"📁 [{folder:<22}] | Arquivos: {len(json_files):2d} | Questões: {total_questions:3d} | Desvios Disciplina: {len(mismatched_discipline):2d} | Desvios Gabarito: {len(mismatched_gabarito):2d} | Status: {status_icon}")

# Print detailed mismatch report
print("\n--- DETALHAMENTO DE DESVIOS ENCONTRADOS ---")
has_any_issues = False
for folder, res in folder_audit_results.items():
    if res['disc_mismatches'] > 0 or res['gab_mismatches'] > 0:
        has_any_issues = True
        print(f"\n🚨 DISCIPLINA: {folder}")
        if res['disc_mismatches'] > 0:
            print(f"   Desvios de Pertinência Temática ({res['disc_mismatches']}):")
            for d in res['mismatched_discipline_details'][:10]:
                print(f"     - Arquivo {d['file']} | {d['exame']} Q{d['num']} | Oficial: \"{d['disc_oficial']}\" -> Na pasta: \"{d['pasta_atual']}\"")
        if res['gab_mismatches'] > 0:
            print(f"   Divergências de Gabarito ({res['gab_mismatches']}):")
            for g in res['mismatched_gabarito_details'][:10]:
                print(f"     - Arquivo {g['file']} | {g['exame']} Q{g['num']} | No arquivo: {g['gab_arquivo']} vs Oficial: {g['gab_oficial']}")

if not has_any_issues:
    print("✨ Nenhuma inconsistência encontrada nas pastas didáticas!")
