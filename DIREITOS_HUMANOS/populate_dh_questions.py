import json
import glob
import os
import subprocess

def classify_dh(q):
    t = (q.get('enunciado', '') + ' ' + str(q.get('tema', ''))).lower()
    
    # 07. Corte Interamericana e Jurisprudência
    if any(k in t for k in ['corte interamericana', 'corte idh', 'tribunal penal internacional', 'tpi ', 'gomes lund', 'fazenda brasil verde', 'vladimir herzog', 'maria da penha', 'condenado pela corte', 'sentença da corte']):
        return '07_cortes_internacionais', 'Corte Interamericana e Jurisprudência'
    # 02. Sistema Interamericano de Direitos Humanos
    elif any(k in t for k in ['sistema interamericano', 'comissão interamericana', 'cidh', 'petição individual', 'relatório de mérito', 'organização dos estados americanos', 'oea']):
        return '02_sistema_interamericano', 'Sistema Interamericano de Direitos Humanos'
    # 06. Pacto de San José da Costa Rica (CADH)
    elif any(k in t for k in ['pacto de san josé', 'convenção americana', 'cadh', 'duplo grau de jurisdição', 'prisão do depositário infiel', 'garantias judiciais']):
        return '06_pacto_san_jose', 'Pacto de San José da Costa Rica (CADH)'
    # 03. Incorporação de Tratados (Art. 5º §3º)
    elif any(k in t for k in ['incorporação', 'art. 5º, § 3º', 'artigo 5º, § 3º', 'quórum de emenda', 'status supralegal', 'controle de convencionalidade', 'ratificação de tratado', 'promulgação de tratado']):
        return '03_incorporacao_tratados', 'Incorporação de Tratados'
    # 04. Proteção a Grupos Vulneráveis e Minorias
    elif any(k in t for k in ['pessoa com deficiência', 'deficiência', 'idoso', 'mulher', 'indígena', 'quilombola', 'refugiado', 'vulnerável', 'criança', 'adolescente', 'migrante']):
        return '04_protecao_vulneraveis', 'Proteção a Grupos Vulneráveis e Minorias'
    # 05. Combate à Tortura e Discriminação
    elif any(k in t for k in ['tortura', 'discriminação', 'igualdade racial', 'racismo', 'genocídio', 'preconceito']):
        return '05_combate_tortura_discriminacao', 'Combate à Tortura e Discriminação'
    # 08. Direitos Humanos na Ordem Constitucional
    elif any(k in t for k in ['incidente de deslocamento de competência', 'idc ', 'pndh', 'programa nacional de direitos humanos', 'constituição da república']):
        return '08_direitos_humanos_brasil', 'Direitos Humanos na Ordem Constitucional'
    # Fallback
    else:
        return '01_conceitos_fundamentais', 'Conceitos Fundamentais e Sistema Global'

def main():
    simulados_files = sorted(glob.glob('/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados/e*_tipo1_branca.json'))
    print(f"📁 Encontrados {len(simulados_files)} arquivos de simulados dos exames.")

    dh_questions = []
    for f in simulados_files:
        filename = os.path.basename(f)
        exame_num = filename.split('e')[1].split('_')[0]
        with open(f, 'r', encoding='utf-8') as fp:
            items = json.load(fp)
            for item in items:
                num = item.get('num', 0)
                disc = item.get('disciplina', '')
                if 'humanos' in disc.lower():
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    dh_questions.append(item)
                elif disc == '' and (exame_num == '37' and 17 <= num <= 18):
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    dh_questions.append(item)

    print(f"✅ Total de questões de Direitos Humanos extraídas: {len(dh_questions)}")

    modules = {
        '01_conceitos_fundamentais': {'title': 'Conceitos Fundamentais e Sistema Global', 'questions': []},
        '02_sistema_interamericano': {'title': 'Sistema Interamericano de Direitos Humanos', 'questions': []},
        '03_incorporacao_tratados': {'title': 'Incorporação de Tratados', 'questions': []},
        '04_protecao_vulneraveis': {'title': 'Proteção a Grupos Vulneráveis e Minorias', 'questions': []},
        '05_combate_tortura_discriminacao': {'title': 'Combate à Tortura e Discriminação', 'questions': []},
        '06_pacto_san_jose': {'title': 'Pacto de San José da Costa Rica (CADH)', 'questions': []},
        '07_cortes_internacionais': {'title': 'Corte Interamericana e Jurisprudência', 'questions': []},
        '08_direitos_humanos_brasil': {'title': 'Direitos Humanos na Ordem Constitucional', 'questions': []}
    }

    for idx, q in enumerate(dh_questions, start=1):
        mod_key, mod_title = classify_dh(q)
        
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
            "fundamentacao": "<p>Convenção Americana sobre Direitos Humanos (CADH) e Constituição Federal de 1988 (Art. 5º, § 3º e Art. 109, V-A).</p>",
            "dica": "<p>Analise a hierarquia dos tratados de direitos humanos, o trâmite na CIDH/Corte IDH e a proteção às minorias.</p>",
            "aula_comentario": f"<p>Comentário em vídeo referente ao {q.get('exame_label')}.</p>",
            "analise": f"<p>Análise detalhada das alternativas A, B, C e D em desenvolvimento.</p>"
        }

        modules[mod_key]['questions'].append(card_q)

    base_dir = '/home/sfy/Corujinha/DIREITOS_HUMANOS'
    for mod_key, data in modules.items():
        json_path = os.path.join(base_dir, f"{mod_key}_questoes.json")
        with open(json_path, 'w', encoding='utf-8') as fp:
            json.dump(data['questions'], fp, ensure_ascii=False, indent=2)
        print(f"📦 {mod_key}_questoes.json populado com {len(data['questions'])} questões.")

    print("\n🔨 Executando compilação do ecossistema Direitos Humanos via build_dh_modules.py...")
    subprocess.run(["python3", os.path.join(base_dir, "build_dh_modules.py")], check=True)
    print("✨ Processo concluído com sucesso!")

if __name__ == '__main__':
    main()
