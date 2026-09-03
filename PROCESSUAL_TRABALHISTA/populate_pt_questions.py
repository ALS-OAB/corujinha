import json
import glob
import os
import subprocess

def classify_pt(q):
    t = (q.get('enunciado', '') + ' ' + str(q.get('tema', ''))).lower()
    
    # 08. Rito Sumaríssimo e Comissão de Conciliação
    if any(k in t for k in ['rito sumaríssimo', 'sumaríssimo', 'comissão de conciliação prévia', 'ccp']):
        return '08_rito_sumarissimo', 'Rito Sumaríssimo e Comissão de Conciliação'
    # 07. Tutela Provisória e Medidas Cautelares / Inquérito
    elif any(k in t for k in ['tutela provisória', 'tutela de urgência', 'tutela de evidência', 'medida cautelar', 'antecipação de tutela', 'liminar', 'inquérito para apuração de falta grave']):
        return '07_cautela_inquerito', 'Tutela Provisória e Medidas Cautelares'
    # 06. Ações Especiais no Processo do Trabalho
    elif any(k in t for k in ['mandado de segurança', 'ação rescisória', 'dissídio coletivo', 'consignação em pagamento', 'ação de cumprimento']):
        return '06_acoes_especiais', 'Ações Especiais no Processo do Trabalho'
    # 05. Execução Trabalhista
    elif any(k in t for k in ['execução', 'agravo de petição', 'penhora', 'embargos à execução', 'liquidação de sentença', 'idpj', 'desconsideração da personalidade']):
        return '05_execucao_trabalhista', 'Execução Trabalhista'
    # 04. Recursos Trabalhistas
    elif any(k in t for k in ['recurso ordinário', 'recurso de revista', 'agravo de instrumento', 'agravo regimental', 'embargos no tst', 'recurso adesivo', 'depósito recursal', 'custas', 'jus postulandi']):
        return '04_recursos_trabalhistas', 'Recursos Trabalhistas'
    # 03. Provas e Perícias no Processo do Trabalho
    elif any(k in t for k in ['prova', 'ônus da prova', 'testemunha', 'depoimento pessoal', 'perícia', 'perito', 'documento', 'exibição de documento']):
        return '03_provas_pericia', 'Provas e Perícias no Processo do Trabalho'
    # 02. Reclamação Trabalhista e Atos Processuais
    elif any(k in t for k in ['reclamação trabalhista', 'petição inicial', 'contestação', 'reconvenção', 'revelia', 'arquivamento', 'audiência', 'acordo', 'conciliação', 'exceção de incompetência', 'notificação', 'citação']):
        return '02_reclamacao_trabalhista', 'Reclamação Trabalhista e Atos Processuais'
    # 01. Organização da Justiça do Trabalho (Fallback / Competência)
    else:
        return '01_organizacao_justica', 'Organização da Justiça do Trabalho'

def main():
    simulados_files = sorted(glob.glob('/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados/e*_tipo1_branca.json'))
    print(f"📁 Encontrados {len(simulados_files)} arquivos de simulados dos exames.")

    pt_questions = []
    for f in simulados_files:
        filename = os.path.basename(f)
        exame_num = filename.split('e')[1].split('_')[0]
        with open(f, 'r', encoding='utf-8') as fp:
            items = json.load(fp)
            for item in items:
                num = item.get('num', 0)
                disc = item.get('disciplina', '')
                if 'process' in disc.lower() and 'trabalho' in disc.lower():
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    pt_questions.append(item)
                elif disc == '' and (exame_num == '37' and 74 <= num <= 80):
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    pt_questions.append(item)

    print(f"✅ Total de questões de Direito Processual do Trabalho extraídas: {len(pt_questions)}")

    modules = {
        '01_organizacao_justica': {'title': 'Organização da Justiça do Trabalho', 'questions': []},
        '02_reclamacao_trabalhista': {'title': 'Reclamação Trabalhista e Atos Processuais', 'questions': []},
        '03_provas_pericia': {'title': 'Provas e Perícias no Processo do Trabalho', 'questions': []},
        '04_recursos_trabalhistas': {'title': 'Recursos Trabalhistas', 'questions': []},
        '05_execucao_trabalhista': {'title': 'Execução Trabalhista', 'questions': []},
        '06_acoes_especiais': {'title': 'Ações Especiais no Processo do Trabalho', 'questions': []},
        '07_cautela_inquerito': {'title': 'Tutela Provisória e Medidas Cautelares', 'questions': []},
        '08_rito_sumarissimo': {'title': 'Rito Sumaríssimo e Comissão de Conciliação', 'questions': []}
    }

    for idx, q in enumerate(pt_questions, start=1):
        mod_key, mod_title = classify_pt(q)
        
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
            "fundamentacao": "<p>Consolidação das Leis do Trabalho (Livro VI - Do Processo do Trabalho) e Súmulas/OJs do TST.</p>",
            "dica": "<p>Analise a competência, os prazos recursais, as nulidades processuais e as regras de execução trabalhista.</p>",
            "aula_comentario": f"<p>Comentário em vídeo referente ao {q.get('exame_label')}.</p>",
            "analise": f"<p>Análise detalhada das alternativas A, B, C e D em desenvolvimento.</p>"
        }

        modules[mod_key]['questions'].append(card_q)

    base_dir = '/home/sfy/Corujinha/PROCESSUAL_TRABALHISTA'
    for mod_key, data in modules.items():
        json_path = os.path.join(base_dir, f"{mod_key}_questoes.json")
        with open(json_path, 'w', encoding='utf-8') as fp:
            json.dump(data['questions'], fp, ensure_ascii=False, indent=2)
        print(f"📦 {mod_key}_questoes.json populado com {len(data['questions'])} questões.")

    print("\n🔨 Executando compilação do ecossistema Processual Trabalhista via build_pt_modules.py...")
    subprocess.run(["python3", os.path.join(base_dir, "build_pt_modules.py")], check=True)
    print("✨ Processo concluído com sucesso!")

if __name__ == '__main__':
    main()
