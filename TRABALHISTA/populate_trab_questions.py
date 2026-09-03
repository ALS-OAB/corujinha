import json
import glob
import os
import subprocess

def classify_trab(q):
    t = (q.get('enunciado', '') + ' ' + str(q.get('tema', ''))).lower()
    
    # 06. Organização Sindical e Negociação Coletiva
    if any(k in t for k in ['sindicat', 'convenção coletiva', 'acordo coletivo', 'negociação coletiva', 'norma coletiva', 'greve', 'contribuição assistencial', 'contribuição sindical']):
        return '06_organizacao_sindical', 'Organização Sindical e Negociação Coletiva'
    # 05. Estabilidades e Garantias de Emprego
    elif any(k in t for k in ['estabilidade', 'gestante', 'maternidade', 'cipa', 'cipista', 'dirigente sindical', 'acidente de trabalho', 'garantia de emprego']):
        return '05_estabilidades_garantias', 'Estabilidades e Garantias de Emprego'
    # 04. Rescisão do Contrato de Trabalho
    elif any(k in t for k in ['rescisão', 'justa causa', 'dispensa', 'demissão', 'rescisão indireta', 'culpa recíproca', 'distrato', 'verbas rescisórias', 'pdv', 'demissão voluntária']):
        return '04_rescisao_contrato', 'Rescisão do Contrato de Trabalho'
    # 03. Férias, 13º Salário e FGTS
    elif any(k in t for k in ['férias', '13º', 'décimo terceiro', 'fgts', 'fundo de garantia', 'abono pecuniário']):
        return '03_ferias_salario', 'Férias, 13º Salário e FGTS'
    # 02. Jornada de Trabalho e Remuneração
    elif any(k in t for k in ['jornada', 'horas extras', 'banco de horas', 'intervalo', 'noturno', 'remuneração', 'salário', 'equiparação salarial', 'adicional', 'insalubridade', 'periculosidade', 'comissão', 'prêmio']):
        return '02_jornada_remuneracao', 'Jornada de Trabalho e Remuneração'
    # 07. Saúde, Segurança e Trabalho Especial (Mulher/Menor/EPI)
    elif any(k in t for k in ['epi', 'equipamento de proteção', 'mulher', 'menor', 'aprendiz', 'segurança do trabalho', 'saúde do trabalhador']):
        return '07_saude_seguranca', 'Saúde, Segurança e Trabalho Especial'
    # 08. Direito Previdenciário Aplicado ao Trabalho
    elif any(k in t for k in ['previdência', 'auxílio', 'incapacidade', 'aposentadoria', 'benefício previdenciário']):
        return '08_previdencia_beneficios', 'Direito Previdenciário Aplicado ao Trabalho'
    # 01. Contrato de Trabalho e Relação de Emprego (Fallback)
    else:
        return '01_contrato_trabalho', 'Contrato de Trabalho e Relação de Emprego'

def main():
    simulados_files = sorted(glob.glob('/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados/e*_tipo1_branca.json'))
    print(f"📁 Encontrados {len(simulados_files)} arquivos de simulados dos exames.")

    trab_questions = []
    for f in simulados_files:
        filename = os.path.basename(f)
        exame_num = filename.split('e')[1].split('_')[0]
        with open(f, 'r', encoding='utf-8') as fp:
            items = json.load(fp)
            for item in items:
                num = item.get('num', 0)
                disc = item.get('disciplina', '')
                if 'trabalho' in disc.lower() and 'process' not in disc.lower():
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    trab_questions.append(item)
                elif disc == '' and (exame_num == '37' and 68 <= num <= 73):
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    trab_questions.append(item)

    print(f"✅ Total de questões de Direito do Trabalho (CLT) extraídas: {len(trab_questions)}")

    modules = {
        '01_contrato_trabalho': {'title': 'Contrato de Trabalho e Relação de Emprego', 'questions': []},
        '02_jornada_remuneracao': {'title': 'Jornada de Trabalho e Remuneração', 'questions': []},
        '03_ferias_salario': {'title': 'Férias, 13º Salário e FGTS', 'questions': []},
        '04_rescisao_contrato': {'title': 'Rescisão do Contrato de Trabalho', 'questions': []},
        '05_estabilidades_garantias': {'title': 'Estabilidades e Garantias de Emprego', 'questions': []},
        '06_organizacao_sindical': {'title': 'Organização Sindical e Negociação Coletiva', 'questions': []},
        '07_saude_seguranca': {'title': 'Saúde, Segurança e Trabalho Especial', 'questions': []},
        '08_previdencia_beneficios': {'title': 'Direito Previdenciário Aplicado ao Trabalho', 'questions': []}
    }

    for idx, q in enumerate(trab_questions, start=1):
        mod_key, mod_title = classify_trab(q)
        
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
            "fundamentacao": "<p>Consolidação das Leis do Trabalho (Decreto-Lei nº 5.452/1943) e Súmulas/OJs do TST.</p>",
            "dica": "<p>Analise a alteração contratual, direitos rescisórios, jornada e a jurisprudência sumulada do TST.</p>",
            "aula_comentario": f"<p>Comentário em vídeo referente ao {q.get('exame_label')}.</p>",
            "analise": f"<p>Análise detalhada das alternativas A, B, C e D em desenvolvimento.</p>"
        }

        modules[mod_key]['questions'].append(card_q)

    base_dir = '/home/sfy/Corujinha/TRABALHISTA'
    for mod_key, data in modules.items():
        json_path = os.path.join(base_dir, f"{mod_key}_questoes.json")
        with open(json_path, 'w', encoding='utf-8') as fp:
            json.dump(data['questions'], fp, ensure_ascii=False, indent=2)
        print(f"📦 {mod_key}_questoes.json populado com {len(data['questions'])} questões.")

    print("\n🔨 Executando compilação do ecossistema Trabalhista via build_trab_modules.py...")
    subprocess.run(["python3", os.path.join(base_dir, "build_trab_modules.py")], check=True)
    print("✨ Processo concluído com sucesso!")

if __name__ == '__main__':
    main()
