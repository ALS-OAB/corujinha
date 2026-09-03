import json
import glob
import os
import subprocess

def classify_cons(q):
    t = (q.get('enunciado', '') + ' ' + str(q.get('tema', ''))).lower()
    
    # 06. Bancos de Dados e Superendividamento
    if any(k in t for k in ['banco de dados', 'cadastro de inadimplente', 'spc', 'serasa', 'superendividamento', 'mínimo existencial', 'repactuação', 'empréstimo']):
        return '06_bancos_dados', 'Cadastros de Inadimplentes e Superendividamento'
    # 03. Responsabilidade pelo Fato e Vício
    elif any(k in t for k in ['fato do produto', 'vício do produto', 'fato do serviço', 'vício do serviço', 'defeito', 'acidente de consumo', 'decadência', 'prescrição', '30 dias', '90 dias', '5 anos', 'estragou', 'danificado', 'garantia', 'reparar']):
        return '03_fato_vicio_produto', 'Responsabilidade pelo Fato e Vício'
    # 05. Cláusulas Abusivas e Contratos
    elif any(k in t for k in ['cláusula abusiva', 'cláusulas abusivas', 'direito de arrependimento', '7 dias', 'contrato de adesão', 'fora do estabelecimento', 'cancelamento']):
        return '05_clausulas_abusivas', 'Cláusulas Abusivas e Contratos'
    # 04. Práticas Comerciais e Publicidade Enganosa
    elif any(k in t for k in ['publicidade enganosa', 'publicidade abusiva', 'oferta', 'venda casada', 'repetição do indébito', 'cobrança de dívida', 'cobrado em dobro']):
        return '04_praticas_comerciais', 'Práticas Comerciais e Publicidade Enganosa'
    # 07. Defesa em Juízo e Ações Coletivas
    elif any(k in t for k in ['desconsideração da personalidade', 'teoria menor', 'ação coletiva', 'tutela coletiva', 'defesa em juízo']):
        return '07_defesa_juizo', 'Defesa em Juízo e Ações Coletivas'
    # 02. Princípios e Direitos Básicos
    elif any(k in t for k in ['direito básico', 'inversão do ônus da prova', 'vulnerabilidade', 'boa-fé objetiva', 'informação']):
        return '02_principios_direitos', 'Princípios e Direitos Básicos'
    # 08. Sanções Administrativas e Crimes de Consumo
    elif any(k in t for k in ['sanção administrativa', 'procon', 'crime contra as relações de consumo', 'infrações penais']):
        return '08_sancoes_crimes', 'Sanções Administrativas e Crimes de Consumo'
    # Fallback
    else:
        return '01_conceitos_fundamentais', 'Conceitos de Consumidor e Fornecedor'

def main():
    simulados_files = sorted(glob.glob('/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados/e*_tipo1_branca.json'))
    print(f"📁 Encontrados {len(simulados_files)} arquivos de simulados dos exames.")

    cons_questions = []
    for f in simulados_files:
        filename = os.path.basename(f)
        exame_num = filename.split('e')[1].split('_')[0]
        with open(f, 'r', encoding='utf-8') as fp:
            items = json.load(fp)
            for item in items:
                num = item.get('num', 0)
                disc = item.get('disciplina', '')
                if 'consumidor' in disc.lower():
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    cons_questions.append(item)
                elif disc == '' and (exame_num == '37' and 42 <= num <= 43):
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    cons_questions.append(item)

    print(f"✅ Total de questões de Direito do Consumidor extraídas: {len(cons_questions)}")

    modules = {
        '01_conceitos_fundamentais': {'title': 'Conceitos de Consumidor e Fornecedor', 'questions': []},
        '02_principios_direitos': {'title': 'Princípios e Direitos Básicos', 'questions': []},
        '03_fato_vicio_produto': {'title': 'Responsabilidade pelo Fato e Vício', 'questions': []},
        '04_praticas_comerciais': {'title': 'Práticas Comerciais e Publicidade Enganosa', 'questions': []},
        '05_clausulas_abusivas': {'title': 'Cláusulas Abusivas e Contratos', 'questions': []},
        '06_bancos_dados': {'title': 'Cadastros de Inadimplentes e Superendividamento', 'questions': []},
        '07_defesa_juizo': {'title': 'Defesa em Juízo e Ações Coletivas', 'questions': []},
        '08_sancoes_crimes': {'title': 'Sanções Administrativas e Crimes de Consumo', 'questions': []}
    }

    for idx, q in enumerate(cons_questions, start=1):
        mod_key, mod_title = classify_cons(q)
        
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
            "fundamentacao": "<p>Código de Defesa do Consumidor (Lei nº 8.078/1990) e Lei do Superendividamento (Lei nº 14.181/2021).</p>",
            "dica": "<p>Observe os prazos para reclamação por vício (30/90 dias) e fato (5 anos), além da responsabilidade objetiva do fornecedor.</p>",
            "aula_comentario": f"<p>Comentário em vídeo referente ao {q.get('exame_label')}.</p>",
            "analise": f"<p>Análise detalhada das alternativas A, B, C e D em desenvolvimento.</p>"
        }

        modules[mod_key]['questions'].append(card_q)

    base_dir = '/home/sfy/Corujinha/CONSUMIDOR'
    for mod_key, data in modules.items():
        json_path = os.path.join(base_dir, f"{mod_key}_questoes.json")
        with open(json_path, 'w', encoding='utf-8') as fp:
            json.dump(data['questions'], fp, ensure_ascii=False, indent=2)
        print(f"📦 {mod_key}_questoes.json populado com {len(data['questions'])} questões.")

    print("\n🔨 Executando compilação do ecossistema Direito do Consumidor via build_cons_modules.py...")
    subprocess.run(["python3", os.path.join(base_dir, "build_cons_modules.py")], check=True)
    print("✨ Processo concluído com sucesso!")

if __name__ == '__main__':
    main()
