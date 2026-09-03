import json
import glob
import os
import subprocess

def classify_etica(q):
    t = (q.get('enunciado', '') + ' ' + str(q.get('tema', ''))).lower()
    
    # 04. Infrações e Sanções Disciplinares
    if any(k in t for k in ['infração', 'infrações', 'sanção', 'sanções', 'censura', 'suspensão', 'exclusão', 'multa disciplinar', 'reabilitação', 'idôneo', 'inépcia', 'repreensão']):
        return '04_infracoes_e_sancoes', 'Infrações e Sanções Disciplinares'
    # 03. Incompatibilidades e Impedimentos
    elif any(k in t for k in ['incompatividad', 'incompatível', 'impedimento', 'impedid', 'servidor público', 'policial', 'magistrado', 'parlamentar', 'cargo de direção', 'chefia do poder executivo']):
        return '03_incompatibilidade_e_impedimento', 'Incompatibilidades e Impedimentos'
    # 02. Direitos e Prerrogativas
    elif any(k in t for k in ['prerrogativa', 'prerrogativas', 'inviolabilidade', 'sigilo profissional', 'imunidade', 'desagravo', 'sala de estado maior', 'cliente preso', 'pela ordem', 'busca e apreensão', 'gestante', 'lactante', 'advogada']):
        return '02_direitos_e_prerrogativas', 'Direitos e Prerrogativas dos Advogados'
    # 05. Sociedades e Honorários
    elif any(k in t for k in ['honorário', 'honorários', 'sociedade de advogados', 'sociedade unipessoal', 'quota litis', 'arbitramento de honorários', 'cobrança de honorários', 'sucumbência']):
        return '05_publicidade_e_honorarios', 'Sociedades de Advogados e Honorários'
    # 06. Publicidade e Marketing Jurídico
    elif any(k in t for k in ['publicidade', 'marketing', 'redes sociais', 'provimento 205', 'captação de cliente', 'anúncio', 'mala direta', 'patrocinado']):
        return '06_publicidade_e_marketing', 'Publicidade e Marketing Jurídico'
    # 08. Processo Administrativo e Eleitoral
    elif any(k in t for k in ['processo disciplinar', 'pad', 'tribunal de ética', 'ted', 'recurso ao conselho', 'prescrição da pretensão punitiva', 'eleição da oab', 'chapa', 'eleitoral']):
        return '08_processo_administrativo_e_eleitoral', 'Processo Eleitoral e Processo Administrativo Disciplinar (PAD)'
    # 01. Órgãos da OAB
    elif any(k in t for k in ['conselho federal', 'conselho seccional', 'subseção', 'caixa de assistência', 'caaf', 'órgão da oab', 'anuidade', 'conferência nacional', 'quinto constitucional']):
        return '01_orgaos_da_oab', 'Órgãos da OAB'
    # Fallback
    else:
        return '07_advogados_e_estagiarios', 'Advogados, Estagiários e Atos Privativos'

def main():
    simulados_files = sorted(glob.glob('/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados/e*_tipo1_branca.json'))
    print(f"📁 Encontrados {len(simulados_files)} arquivos de simulados dos exames.")

    etica_questions = []

    for f in simulados_files:
        filename = os.path.basename(f)
        exame_num = int(filename.split('e')[1].split('_')[0])
        with open(f, 'r', encoding='utf-8') as fp:
            items = json.load(fp)
            q_by_num = {}
            for q in items:
                num = q.get('num', 0)
                if 1 <= num <= 8:
                    if num not in q_by_num:
                        q['exame_num'] = exame_num
                        q['exame_label'] = f'{exame_num}º Exame OAB'
                        q_by_num[num] = q
            for num in sorted(q_by_num.keys()):
                etica_questions.append(q_by_num[num])

    print(f"✅ Total de questões de Ética Profissional extraídas: {len(etica_questions)}")

    modules = {
        '01_orgaos_da_oab': {'title': 'Órgãos da OAB', 'questions': []},
        '02_direitos_e_prerrogativas': {'title': 'Direitos e Prerrogativas dos Advogados', 'questions': []},
        '03_incompatibilidade_e_impedimento': {'title': 'Incompatibilidades e Impedimentos', 'questions': []},
        '04_infracoes_e_sancoes': {'title': 'Infrações e Sanções Disciplinares', 'questions': []},
        '05_publicidade_e_honorarios': {'title': 'Sociedades de Advogados e Honorários', 'questions': []},
        '06_publicidade_e_marketing': {'title': 'Publicidade e Marketing Jurídico', 'questions': []},
        '07_advogados_e_estagiarios': {'title': 'Advogados, Estagiários e Atos Privativos', 'questions': []},
        '08_processo_administrativo_e_eleitoral': {'title': 'Processo Eleitoral e Processo Administrativo Disciplinar (PAD)', 'questions': []}
    }

    for idx, q in enumerate(etica_questions, start=1):
        mod_key, mod_title = classify_etica(q)
        
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
            "fundamentacao": "<p>Estatuto da Advocacia e da OAB (Lei nº 8.906/1994), Código de Ética e Disciplina e Regulamento Geral da OAB.</p>",
            "dica": "<p>Atenção especial às prerrogativas da advogada gestante e regras de sanções disciplinadas (censura, suspensão e exclusão).</p>",
            "aula_comentario": f"<p>Comentário em vídeo referente ao {q.get('exame_label')}.</p>",
            "analise": f"<p>Análise detalhada das alternativas A, B, C e D em desenvolvimento.</p>"
        }

        modules[mod_key]['questions'].append(card_q)

    base_dir = '/home/sfy/Corujinha/ETICA'
    for mod_key, data in modules.items():
        json_path = os.path.join(base_dir, f"{mod_key}_questoes.json")
        with open(json_path, 'w', encoding='utf-8') as fp:
            json.dump(data['questions'], fp, ensure_ascii=False, indent=2)
        print(f"📦 {mod_key}_questoes.json populado com {len(data['questions'])} questões.")

    print("\n🔨 Executando compilação do ecossistema Ética Profissional via build_all_modules.py...")
    subprocess.run(["python3", os.path.join(base_dir, "build_all_modules.py")], check=True)
    print("✨ Processo concluído com sucesso!")

if __name__ == '__main__':
    main()
