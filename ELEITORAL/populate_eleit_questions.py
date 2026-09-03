import json
import glob
import os
import subprocess

def classify_eleit(q):
    t = (q.get('enunciado', '') + ' ' + str(q.get('tema', ''))).lower()
    
    # 07. Ações Eleitorais (AIJE, AIME)
    if any(k in t for k in ['aije', 'aime', 'rced', 'impugnação de mandato', 'investigação judicial eleitoral', 'abuso de poder', 'cassação']):
        return '07_acoes_eleitorais', 'Ações Eleitorais (AIJE, AIME e Representações)'
    # 03. Elegibilidade e Inelegibilidades
    elif any(k in t for k in ['elegibilidade', 'inelegibilidade', 'inelegível', 'ficha limpa', 'lc 64', 'desincompatibilização', 'idade mínima', 'prefeito itinerante', 'reeleição', 'cargo de executivo', 'parentesco']):
        return '03_elegibilidade_inelegibilidades', 'Condições de Elegibilidade e Inelegibilidades'
    # 05. Propaganda Eleitoral
    elif any(k in t for k in ['propaganda eleitoral', 'propaganda na internet', 'horário gratuito', 'direito de resposta', 'extemporânea', 'impulsionamento', 'santinho', 'comício']):
        return '05_propaganda_eleitoral', 'Propaganda Eleitoral (Lei 9.504/97)'
    # 06. Financiamento de Campanha e Contas
    elif any(k in t for k in ['financiamento', 'fundo partidário', 'fundo especial', 'prestação de contas', 'doação', 'gastos de campanha', 'recursos de campanha']):
        return '06_financiamento_contas', 'Financiamento de Campanha e Contas'
    # 04. Partidos Políticos e Federações
    elif any(k in t for k in ['federação', 'fidelidade partidária', 'cláusula de barreira', 'convenção partidária', 'cota de gênero', 'candidatura feminina', 'registro de candidatura', 'coligação']):
        return '04_partidos_federacoes', 'Partidos Políticos e Federações'
    # 08. Crimes Eleitorais
    elif any(k in t for k in ['crime eleitoral', 'crimes eleitorais', 'compra de voto', 'corrupção eleitoral', 'violência política']):
        return '08_crimes_eleitorais', 'Crimes Eleitorais e Processo'
    # 02. Direitos Políticos e Alistamento
    elif any(k in t for k in ['alistamento', 'direitos políticos', 'domicílio eleitoral', 'quitação eleitoral', 'título de eleitor', 'voto facultativo', 'capacidade eleitoral']):
        return '02_direitos_politicos', 'Direitos Políticos e Alistamento'
    # Fallback
    else:
        return '01_principios_justica', 'Princípios e Justiça Eleitoral'

def main():
    simulados_files = sorted(glob.glob('/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados/e*_tipo1_branca.json'))
    print(f"📁 Encontrados {len(simulados_files)} arquivos de simulados dos exames.")

    eleit_questions = []

    for f in simulados_files:
        filename = os.path.basename(f)
        exame_num = filename.split('e')[1].split('_')[0]
        with open(f, 'r', encoding='utf-8') as fp:
            items = json.load(fp)
            for item in items:
                disc = item.get('disciplina', '')
                if 'eleitoral' in disc.lower():
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    eleit_questions.append(item)

    print(f"✅ Total de questões de Direito Eleitoral extraídas: {len(eleit_questions)}")

    modules = {
        '01_principios_justica': {'title': 'Princípios e Justiça Eleitoral', 'questions': []},
        '02_direitos_politicos': {'title': 'Direitos Políticos e Alistamento', 'questions': []},
        '03_elegibilidade_inelegibilidades': {'title': 'Condições de Elegibilidade e Inelegibilidades', 'questions': []},
        '04_partidos_federacoes': {'title': 'Partidos Políticos e Federações', 'questions': []},
        '05_propaganda_eleitoral': {'title': 'Propaganda Eleitoral (Lei 9.504/97)', 'questions': []},
        '06_financiamento_contas': {'title': 'Financiamento de Campanha e Contas', 'questions': []},
        '07_acoes_eleitorais': {'title': 'Ações Eleitorais (AIJE, AIME e Representações)', 'questions': []},
        '08_crimes_eleitorais': {'title': 'Crimes Eleitorais e Processo', 'questions': []}
    }

    for idx, q in enumerate(eleit_questions, start=1):
        mod_key, mod_title = classify_eleit(q)
        
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
            "fundamentacao": "<p>Código Eleitoral (Lei nº 4.737/1965), Lei das Eleições (Lei nº 9.504/1997) e Lei das Inelegibilidades (LC nº 64/1990).</p>",
            "dica": "<p>Observe os prazos de desincompatibilização, hipóteses de inelegibilidade reflexa e regras da Lei da Ficha Limpa.</p>",
            "aula_comentario": f"<p>Comentário em vídeo referente ao {q.get('exame_label')}.</p>",
            "analise": f"<p>Análise detalhada das alternativas A, B, C e D em desenvolvimento.</p>"
        }

        modules[mod_key]['questions'].append(card_q)

    base_dir = '/home/sfy/Corujinha/ELEITORAL'
    for mod_key, data in modules.items():
        json_path = os.path.join(base_dir, f"{mod_key}_questoes.json")
        with open(json_path, 'w', encoding='utf-8') as fp:
            json.dump(data['questions'], fp, ensure_ascii=False, indent=2)
        print(f"📦 {mod_key}_questoes.json populado com {len(data['questions'])} questões.")

    print("\n🔨 Executando compilação do ecossistema Direito Eleitoral via build_eleit_modules.py...")
    subprocess.run(["python3", os.path.join(base_dir, "build_eleit_modules.py")], check=True)
    print("✨ Processo concluído com sucesso!")

if __name__ == '__main__':
    main()
