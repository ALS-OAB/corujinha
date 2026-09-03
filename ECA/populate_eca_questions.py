import json
import glob
import os
import subprocess

def classify_eca(q):
    t = (q.get('enunciado', '') + ' ' + str(q.get('tema', ''))).lower()
    
    # 05. Ato Infracional e Medidas Socioeducativas
    if any(k in t for k in ['ato infracional', 'medida socioeducativa', 'socioeducativ', 'internação', 'semiliberdade', 'liberdade assistida', 'prestação de serviços', 'sinase', 'apreensão de menor', 'adolescente apreendido']):
        return '05_ato_infracional', 'Ato Infracional e Medidas Socioeducativas'
    # 04. Guarda, Tutela e Adoção
    elif any(k in t for k in ['adoção', 'adotou', 'adotado', 'guarda', 'tutela', 'estágio de convivência', 'cadastro de adoção']):
        return '04_guarda_tutela_adocao', 'Guarda, Tutela e Adoção'
    # 03. Convivência Familiar e Comunitária
    elif any(k in t for k in ['convivência familiar', 'família substituta', 'família natural', 'poder familiar', 'destituição do poder familiar', 'suspensão do poder familiar', 'pais', 'mãe biológica', 'pai biológico']):
        return '03_convivencia_familiar', 'Convivência Familiar e Comunitária'
    # 06. Medidas de Proteção e Conselho Tutelar
    elif any(k in t for k in ['conselho tutelar', 'conselheiro tutelar', 'medida de proteção', 'acolhimento institucional', 'acolhimento familiar', 'abrigamento']):
        return '06_medidas_protecao', 'Medidas de Proteção e Conselho Tutelar'
    # 07. Crimes e Infrações no ECA
    elif any(k in t for k in ['crime', 'infração administrativa', 'pornografia', 'bebida alcoólica', 'viagem de menor', 'autorização de viagem', 'hospedagem']):
        return '07_crimes_infracoes', 'Crimes e Infrações no ECA'
    # 08. Justiça da Infância e da Juventude
    elif any(k in t for k in ['justiça da infância', 'vara da infância', 'juiz da infância', 'recurso no eca', 'procedimento infracional', 'prazo recursal']):
        return '08_justica_infancia', 'Justiça da Infância e da Juventude'
    # 02. Direitos Fundamentais da Criança
    elif any(k in t for k in ['direito à vida', 'direito à saúde', 'educação', 'trabalho infantil', 'profissionalização', 'escola', 'matrícula']):
        return '02_direitos_fundamentais', 'Direitos Fundamentais da Criança'
    # Fallback
    else:
        return '01_protecao_integral', 'Proteção Integral e Prioridade Absoluta'

def main():
    simulados_files = sorted(glob.glob('/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados/e*_tipo1_branca.json'))
    print(f"📁 Encontrados {len(simulados_files)} arquivos de simulados dos exames.")

    eca_questions = []
    for f in simulados_files:
        filename = os.path.basename(f)
        exame_num = filename.split('e')[1].split('_')[0]
        with open(f, 'r', encoding='utf-8') as fp:
            items = json.load(fp)
            for item in items:
                num = item.get('num', 0)
                disc = item.get('disciplina', '')
                if 'criança' in disc.lower() or 'eca' in disc.lower() or 'adolescente' in disc.lower():
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    eca_questions.append(item)
                elif disc == '' and (exame_num == '37' and 40 <= num <= 41):
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    eca_questions.append(item)

    print(f"✅ Total de questões de ECA extraídas: {len(eca_questions)}")

    modules = {
        '01_protecao_integral': {'title': 'Proteção Integral e Prioridade Absoluta', 'questions': []},
        '02_direitos_fundamentais': {'title': 'Direitos Fundamentais da Criança', 'questions': []},
        '03_convivencia_familiar': {'title': 'Convivência Familiar e Comunitária', 'questions': []},
        '04_guarda_tutela_adocao': {'title': 'Guarda, Tutela e Adoção', 'questions': []},
        '05_ato_infracional': {'title': 'Ato Infracional e Medidas Socioeducativas', 'questions': []},
        '06_medidas_protecao': {'title': 'Medidas de Proteção e Conselho Tutelar', 'questions': []},
        '07_crimes_infracoes': {'title': 'Crimes e Infrações no ECA', 'questions': []},
        '08_justica_infancia': {'title': 'Justiça da Infância e da Juventude', 'questions': []}
    }

    for idx, q in enumerate(eca_questions, start=1):
        mod_key, mod_title = classify_eca(q)
        
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
            "fundamentacao": "<p>Estatuto da Criança e do Adolescente (Lei nº 8.069/1990) e Lei do SINASE (Lei nº 12.594/2012).</p>",
            "dica": "<p>Atente-se para os limites das medidas socioeducativas, prazos de internação provisória (45 dias) e regras de adoção.</p>",
            "aula_comentario": f"<p>Comentário em vídeo referente ao {q.get('exame_label')}.</p>",
            "analise": f"<p>Análise detalhada das alternativas A, B, C e D em desenvolvimento.</p>"
        }

        modules[mod_key]['questions'].append(card_q)

    base_dir = '/home/sfy/Corujinha/ECA'
    for mod_key, data in modules.items():
        json_path = os.path.join(base_dir, f"{mod_key}_questoes.json")
        with open(json_path, 'w', encoding='utf-8') as fp:
            json.dump(data['questions'], fp, ensure_ascii=False, indent=2)
        print(f"📦 {mod_key}_questoes.json populado com {len(data['questions'])} questões.")

    print("\n🔨 Executando compilação do ecossistema ECA via build_eca_modules.py...")
    subprocess.run(["python3", os.path.join(base_dir, "build_eca_modules.py")], check=True)
    print("✨ Processo concluído com sucesso!")

if __name__ == '__main__':
    main()
