import json
import glob
import os
import subprocess

def classify_prev(q):
    t = (q.get('enunciado', '') + ' ' + str(q.get('tema', ''))).lower()
    
    # 05. Aposentadorias e Incapacidade
    if any(k in t for k in ['aposentadoria', 'incapacidade permanente', 'invalidez', 'auxílio-doença', 'incapacidade temporária', 'auxílio-acidente', 'acidente de trabalho', 'reabilitação']):
        return '05_aposentadorias_incapacidade', 'Aposentadorias e Incapacidade'
    # 06. Pensão por Morte e Auxílios
    elif any(k in t for k in ['pensão por morte', 'auxílio-reclusão', 'salário-maternidade', 'salário-família', 'morte do segurado']):
        return '06_pensao_morte_auxilios', 'Pensão por Morte e Auxílios'
    # 04. Carência e Qualidade de Segurado
    elif any(k in t for k in ['carência', 'período de graça', 'qualidade de segurado', 'manutenção da qualidade', 'perda da qualidade', 'meses de contribuição']):
        return '04_carencia_qualidade', 'Carência e Qualidade de Segurado'
    # 02. Segurados e Dependentes do RGPS
    elif any(k in t for k in ['segurado especial', 'contribuinte individual', 'empregado doméstico', 'segurado facultativo', 'trabalhador avulso', 'dependente', 'qualidade de dependente', 'cônjuge', 'companheira', 'filho menor']):
        return '02_segurados_rgps', 'Segurados e Dependentes do RGPS'
    # 07. Reforma Previdenciária (EC 103/2019)
    elif any(k in t for k in ['ec 103', 'reforma da previdência', 'regra de transição', 'pedágio', 'pontos', 'emenda constitucional 103', 'transição']):
        return '07_reforma_ec103', 'Reforma Previdenciária (EC 103/2019)'
    # 03. Financiamento e Contribuições Sociais
    elif any(k in t for k in ['contribuição social', 'salário de contribuição', 'custeio', 'alíquota', 'isenção', 'patronal', 'arrecadação', 'recolher']):
        return '03_financiamento_contribuicoes', 'Financiamento e Contribuições Sociais'
    # 08. Processo Previdenciario
    elif any(k in t for k in ['processo administrativo', 'inss', 'crps', 'requerimento administrativo', 'prescrição quinquenal', 'decadência', 'indeferimento']):
        return '08_processo_previdenciario', 'Processo Previdenciário Administrativo e Judicial'
    # Fallback
    else:
        return '01_seguridade_social', 'Seguridade Social e Princípios'

def main():
    simulados_files = sorted(glob.glob('/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados/e*_tipo1_branca.json'))
    print(f"📁 Encontrados {len(simulados_files)} arquivos de simulados dos exames.")

    prev_questions = []

    for f in simulados_files:
        filename = os.path.basename(f)
        exame_num = filename.split('e')[1].split('_')[0]
        with open(f, 'r', encoding='utf-8') as fp:
            items = json.load(fp)
            for item in items:
                disc = item.get('disciplina', '')
                if 'previdenciário' in disc.lower() or 'previdenciario' in disc.lower():
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    prev_questions.append(item)

    print(f"✅ Total de questões de Direito Previdenciário extraídas: {len(prev_questions)}")

    modules = {
        '01_seguridade_social': {'title': 'Seguridade Social e Princípios', 'questions': []},
        '02_segurados_rgps': {'title': 'Segurados e Dependentes do RGPS', 'questions': []},
        '03_financiamento_contribuicoes': {'title': 'Financiamento e Contribuições Sociais', 'questions': []},
        '04_carencia_qualidade': {'title': 'Carência e Qualidade de Segurado', 'questions': []},
        '05_aposentadorias_incapacidade': {'title': 'Aposentadorias e Incapacidade', 'questions': []},
        '06_pensao_morte_auxilios': {'title': 'Pensão por Morte e Auxílios', 'questions': []},
        '07_reforma_ec103': {'title': 'Reforma Previdenciária (EC 103/2019)', 'questions': []},
        '08_processo_previdenciario': {'title': 'Processo Previdenciário Administrativo e Judicial', 'questions': []}
    }

    for idx, q in enumerate(prev_questions, start=1):
        mod_key, mod_title = classify_prev(q)
        
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
            "fundamentacao": "<p>Lei de Benefícios (Lei nº 8.213/1991), Lei de Custeio (Lei nº 8.212/1991) e Emenda Constitucional nº 103/2019.</p>",
            "dica": "<p>Atente para a carência exigida nos benefícios por incapacidade e regras de acumulação estabelecidas pela Reforma.</p>",
            "aula_comentario": f"<p>Comentário em vídeo referente ao {q.get('exame_label')}.</p>",
            "analise": f"<p>Análise detalhada das alternativas A, B, C e D em desenvolvimento.</p>"
        }

        modules[mod_key]['questions'].append(card_q)

    base_dir = '/home/sfy/Corujinha/PREVIDENCIARIO'
    for mod_key, data in modules.items():
        json_path = os.path.join(base_dir, f"{mod_key}_questoes.json")
        with open(json_path, 'w', encoding='utf-8') as fp:
            json.dump(data['questions'], fp, ensure_ascii=False, indent=2)
        print(f"📦 {mod_key}_questoes.json populado com {len(data['questions'])} questões.")

    print("\n🔨 Executando compilação do ecossistema Direito Previdenciário via build_prev_modules.py...")
    subprocess.run(["python3", os.path.join(base_dir, "build_prev_modules.py")], check=True)
    print("✨ Processo concluído com sucesso!")

if __name__ == '__main__':
    main()
