import json
import glob
import os
import subprocess

def classify_cpc(q):
    t = (q.get('enunciado', '') + ' ' + q.get('tema', '')).lower()
    
    # 07. Recursos e Tribunais
    if any(k in t for k in ['recurso', 'apelaç', 'agravo', 'embargos de declaraç', 'recurso especial', 'recurso extraordinário', 'efeito suspensivo', 'acórdão']):
        return '07_recursos_tribunais', 'Processo nos Tribunais e Recursos'
    # 06. Execução e Cumprimento de Sentença
    elif any(k in t for k in ['execuç', 'cumprimento de sentença', 'impugnaç', 'título executivo', 'penhora', 'exequente', 'executado', 'embargos à execuç']):
        return '06_execucao_cumprimento', 'Cumprimento de Sentença e Execução'
    # 04. Tutela Provisória
    elif any(k in t for k in ['tutela', 'urgênc', 'evidênc', 'cautelar', 'antecipada', 'liminar']):
        return '04_tutela_provisoria', 'Tutela Provisória (Urgência e Evidência)'
    # 08. Procedimentos Especiais
    elif any(k in t for k in ['monitór', 'possessór', 'inventári', 'exigir contas', 'consignaç', 'embargos de terceiro', 'despejo', 'dissoluç']):
        return '08_procedimentos_especiais', 'Procedimentos Especiais e Juizados'
    # 03. Competência e Atos Processuais
    elif any(k in t for k in ['competênc', 'foro', 'domicílio', 'prazo', 'tempestiv', 'preclusã', 'intimação', 'nulidade', 'comunicação dos atos', 'carta precatória', 'aracaju', 'salvador', 'fortaleza', 'rio de janeiro']):
        return '03_competencia_atos', 'Competência e Atos Processuais'
    # 02. Partes, Procuradores e Litisconsórcio / Intervenção de Terceiros
    elif any(k in t for k in ['litisconsór', 'denunciaç', 'chamamento', 'assistênc', 'desconsideraç', 'amicus curiae', 'capacidad', 'legitimidad', 'advogado', 'procurador', 'impedimento', 'suspeição']):
        return '02_partes_litisconsorcio', 'Partes, Procuradores e Litisconsórcio'
    # 05. Procedimento Comum
    elif any(k in t for k in ['petição inicial', 'contestac', 'reconvenç', 'revelia', 'saneamento', 'audiência', 'citac', 'citação', 'réu', 'indenizatório']):
        return '05_procedimento_comum', 'Procedimento Comum'
    # 01. Normas Fundamentais e Jurisdição (Fallback)
    else:
        return '01_normas_fundamentais', 'Normas Fundamentais e Jurisdição'

def main():
    simulados_files = sorted(glob.glob('/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados/e*_tipo1_branca.json'))
    print(f"📁 Encontrados {len(simulados_files)} arquivos de simulados dos exames.")

    cpc_questions = []
    for f in simulados_files:
        filename = os.path.basename(f)
        exame_num = filename.split('e')[1].split('_')[0]
        with open(f, 'r', encoding='utf-8') as fp:
            items = json.load(fp)
            for item in items:
                disc = item.get('disciplina', '')
                num = item.get('num', 0)
                
                # Filter out misclassified Empresarial questions in E37
                if int(exame_num) == 37 and num in [49, 50, 51]:
                    continue
                
                if disc == 'Processo Civil' or (disc == '' and 51 <= num <= 56):
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    cpc_questions.append(item)

    print(f"✅ Total de questões de Processo Civil extraídas: {len(cpc_questions)}")

    modules = {
        '01_normas_fundamentais': {'title': 'Normas Fundamentais e Jurisdição', 'questions': []},
        '02_partes_litisconsorcio': {'title': 'Partes, Procuradores e Litisconsórcio', 'questions': []},
        '03_competencia_atos': {'title': 'Competência e Atos Processuais', 'questions': []},
        '04_tutela_provisoria': {'title': 'Tutela Provisória (Urgência e Evidência)', 'questions': []},
        '05_procedimento_comum': {'title': 'Procedimento Comum', 'questions': []},
        '06_execucao_cumprimento': {'title': 'Cumprimento de Sentença e Execução', 'questions': []},
        '07_recursos_tribunais': {'title': 'Processo nos Tribunais e Recursos', 'questions': []},
        '08_procedimentos_especiais': {'title': 'Procedimentos Especiais e Juizados', 'questions': []}
    }

    for idx, q in enumerate(cpc_questions, start=1):
        mod_key, mod_title = classify_cpc(q)
        
        # Build options dictionary
        opcoes = {}
        for opt in ['A', 'B', 'C', 'D']:
            val = q.get(f'opcao_{opt.lower()}') or q.get('opcoes', {}).get(opt, f'Opção {opt}')
            opcoes[opt] = val

        gabarito = q.get('gabarito', 'A').upper()
        if gabarito not in ['A', 'B', 'C', 'D']:
            gabarito = 'A'

        card_q = {
            "num": len(modules[mod_key]['questions']) + 1,
            "id": idx,
            "exame": q.get('exame_label', f"{q.get('exame_num')}º Exame OAB"),
            "tema": f"{q.get('tema') or mod_title} ({q.get('exame_label')})",
            "enunciado": q.get('enunciado', ''),
            "opcoes": opcoes,
            "gabarito": gabarito,
            "core": True,
            "sintese": f"<p><strong>Aguardando síntese didática / lógica do conceito.</strong><br>Questão oficial extraída do {q.get('exame_label')}. Gabarito definitivo: <strong>Alternativa {gabarito}</strong>.</p>",
            "logica_conceito": f"<p>Fundamentação teórica do tema <em>{q.get('tema') or mod_title}</em> pendente de elaboração pedagógica.</p>",
            "fundamentacao": "<p>Lei nº 13.105/2015 (Código de Processo Civil - CPC).</p>",
            "dica": "<p>Observe atentamente a regra processual aplicável e a jurisprudência consolidada do STJ.</p>",
            "aula_comentario": f"<p>Comentário em vídeo referente ao {q.get('exame_label')}.</p>",
            "analise": f"<p>Análise detalhada das alternativas A, B, C e D em desenvolvimento.</p>"
        }

        modules[mod_key]['questions'].append(card_q)

    base_dir = '/home/sfy/Corujinha/CPC'
    for mod_key, data in modules.items():
        json_path = os.path.join(base_dir, f"{mod_key}_questoes.json")
        with open(json_path, 'w', encoding='utf-8') as fp:
            json.dump(data['questions'], fp, ensure_ascii=False, indent=2)
        print(f"📦 {mod_key}_questoes.json populado com {len(data['questions'])} questões.")

    print("\n🔨 Executando compilação do ecossistema CPC via build_cpc_modules.py...")
    subprocess.run(["python3", os.path.join(base_dir, "build_cpc_modules.py")], check=True)
    print("✨ Processo concluído com sucesso!")

if __name__ == '__main__':
    main()
