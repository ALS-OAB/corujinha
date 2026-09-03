import json
import glob
import os
import subprocess

def classify_cpp(q):
    t = (q.get('enunciado', '') + ' ' + str(q.get('tema', ''))).lower()
    
    # 03. Prisão e Medidas Cautelares
    if any(k in t for k in ['prisão em flagrante', 'prisão preventiva', 'prisão temporária', 'liberdade provisória', 'fiança', 'audiência de custódia', 'medida cautelar diversa', 'relaxamento da prisão']):
        return '03_prisao_cautelares', 'Prisão e Medidas Cautelares'
    # 08. Juizado Especial Criminal e Lei Maria da Penha / Execução Penal
    elif any(k in t for k in ['juizado especial', '9.099', 'transação penal', 'composição civil', 'suspensão condicional do processo', 'maria da penha', 'execução penal', 'lep ', 'progressão de regime']):
        return '08_juizado_especial', 'Juizado Especial Criminal e Lei Maria da Penha'
    # 07. Recursos Penais e Ações Autônomas
    elif any(k in t for k in ['recurso em sentido estrito', 'rese ', 'apelação', 'embargos de declaração', 'embargos infringentes', 'carta testemunhável', 'revisão criminal', 'habeas corpus', 'recurso especial', 'recurso extraordinário', 'agravo em execução']):
        return '07_recursos_penais', 'Recursos Penais'
    # 04. Provas no Processo Penal
    elif any(k in t for k in ['busca e apreensão', 'perícia', 'corpo de delito', 'testemunha', 'reconhecimento de pessoas', 'cadeia de custódia', 'prova ilícita', 'interceptação telefônica']):
        return '04_provas_processo_penal', 'Provas no Processo Penal'
    # 05. Procedimentos Penais / Tribunal do Júri
    elif any(k in t for k in ['procedimento comum', 'tribunal do júri', 'júri', 'pronúncia', 'impronúncia', 'desclassificação', 'quesito', 'resposta à acusação', 'citação']):
        return '05_procedimentos_penais', 'Procedimentos Penais'
    # 06. Nulidades e Decisões Penais
    elif any(k in t for k in ['nulidade', 'sentença', 'emendatio libelli', 'mutatio libelli', 'coisa julgada', 'absolvição sumária']):
        return '06_nulidades_decisoes', 'Nulidades e Decisões Penais'
    # 02. Competência e Jurisdição
    elif any(k in t for k in ['competência', 'justiça federal', 'justiça estadual', 'conexão', 'continência', 'foro por prerrogativa', 'prevenção']):
        return '02_competencia_jurisdicao', 'Competência e Jurisdição'
    # 01. Inquérito Policial e Ação Penal (Fallback)
    else:
        return '01_inquerito_acao_penal', 'Inquérito Policial e Ação Penal'

def main():
    simulados_files = sorted(glob.glob('/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados/e*_tipo1_branca.json'))
    print(f"📁 Encontrados {len(simulados_files)} arquivos de simulados dos exames.")

    cpp_questions = []
    for f in simulados_files:
        filename = os.path.basename(f)
        exame_num = filename.split('e')[1].split('_')[0]
        with open(f, 'r', encoding='utf-8') as fp:
            items = json.load(fp)
            for item in items:
                num = item.get('num', 0)
                if (exame_num == '37' and 62 <= num <= 67) or (exame_num != '37' and 63 <= num <= 68):
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    cpp_questions.append(item)

    print(f"✅ Total de questões de Direito Processual Penal (CPP) extraídas: {len(cpp_questions)}")

    modules = {
        '01_inquerito_acao_penal': {'title': 'Inquérito Policial e Ação Penal', 'questions': []},
        '02_competencia_jurisdicao': {'title': 'Competência e Jurisdição', 'questions': []},
        '03_prisao_cautelares': {'title': 'Prisão e Medidas Cautelares', 'questions': []},
        '04_provas_processo_penal': {'title': 'Provas no Processo Penal', 'questions': []},
        '05_procedimentos_penais': {'title': 'Procedimentos Penais', 'questions': []},
        '06_nulidades_decisoes': {'title': 'Nulidades e Decisões Penais', 'questions': []},
        '07_recursos_penais': {'title': 'Recursos Penais', 'questions': []},
        '08_juizado_especial': {'title': 'Juizado Especial Criminal e Lei Maria da Penha', 'questions': []}
    }

    for idx, q in enumerate(cpp_questions, start=1):
        mod_key, mod_title = classify_cpp(q)
        
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
            "fundamentacao": "<p>Código de Processo Penal Brasileiro (Decreto-Lei nº 3.689/1941).</p>",
            "dica": "<p>Observe o rito processual, os prazos, as garantias constitucionais e as regras procedimentais aplicáveis.</p>",
            "aula_comentario": f"<p>Comentário em vídeo referente ao {q.get('exame_label')}.</p>",
            "analise": f"<p>Análise detalhada das alternativas A, B, C e D em desenvolvimento.</p>"
        }

        modules[mod_key]['questions'].append(card_q)

    base_dir = '/home/sfy/Corujinha/PROCESSUAL_PENAL'
    for mod_key, data in modules.items():
        json_path = os.path.join(base_dir, f"{mod_key}_questoes.json")
        with open(json_path, 'w', encoding='utf-8') as fp:
            json.dump(data['questions'], fp, ensure_ascii=False, indent=2)
        print(f"📦 {mod_key}_questoes.json populado com {len(data['questions'])} questões.")

    print("\n🔨 Executando compilação do ecossistema CPP via build_cpp_modules.py...")
    subprocess.run(["python3", os.path.join(base_dir, "build_cpp_modules.py")], check=True)
    print("✨ Processo concluído com sucesso!")

if __name__ == '__main__':
    main()
