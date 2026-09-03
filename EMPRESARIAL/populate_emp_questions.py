import json
import glob
import os
import subprocess

def classify_emp(q):
    t = (q.get('enunciado', '') + ' ' + str(q.get('tema', ''))).lower()
    
    # 06. Falência e Recuperação Judicial
    if any(k in t for k in ['falência', 'recuperação judicial', 'recuperação extrajudicial', 'assembleia de credores', 'credores', 'administrador judicial', 'falido', 'inadimplemento da recuperação']):
        return '06_falencia_recuperacao', 'Falência e Recuperação Judicial'
    # 05. Sociedade Anônima
    elif any(k in t for k in ['sociedade anônima', ' s.a.', ' s/a', 'companhia', 'acionista', 'debenture', 'valores mobiliários']):
        return '05_sociedade_anonima', 'Sociedade Anônima'
    # 03. Títulos de Crédito
    elif any(k in t for k in ['título de crédito', 'nota promissória', 'cheque', 'duplicata', 'letra de câmbio', 'endosso', 'aval', 'aceite', 'protesto']):
        return '03_titulos_credito', 'Títulos de Crédito'
    # 04. Contratos Empresariais
    elif any(k in t for k in ['contrato de comissão', 'representação comercial', 'franquia', 'leasing', 'fatorização', 'factoring', 'alienação fiduciária']):
        return '04_contratos_empresariais', 'Contratos Empresariais'
    # 08. Propriedade Intelectual e Concorrência Desleal
    elif any(k in t for k in ['patente', 'invenção', 'modelo de utilidade', 'marca', 'inpi', 'concorrência desleal', 'propriedade industrial']):
        return '08_propriedade_intelectual', 'Propriedade Intelectual e Concorrência Desleal'
    # 01. Empresário e Sociedades Empresárias
    elif any(k in t for k in ['sociedade limitada', 'sociedade simples', 'sociedade em nome coletivo', 'sócios', 'sócio', 'quota', 'quotas', 'unipessoal', 'alterar a forma', 'caracterização do empresário', 'elemento de empresa', 'emprensarial em nome próprio']):
        return '01_empresario_sociedades', 'Empresário e Sociedades Empresárias'
    # 02. Estabelecimento e Nome Empresarial
    elif any(k in t for k in ['estabelecimento', 'trespasse', 'nome empresarial', 'firma', 'denominação', 'junta comercial', 'registro público de empresas', 'registro mercantil']):
        return '02_estabelecimento_nome', 'Estabelecimento e Nome Empresarial'
    # 07. Direito do Consumidor Aplicado à Empresa
    elif any(k in t for k in ['relação de consumo', 'fornecedor', 'vício do produto', 'fato do produto']):
        return '07_direito_consumidor', 'Direito do Consumidor aplicado à Empresa'
    # Fallback
    else:
        return '01_empresario_sociedades', 'Empresário e Sociedades Empresárias'

def main():
    simulados_files = sorted(glob.glob('/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados/e*_tipo1_branca.json'))
    print(f"📁 Encontrados {len(simulados_files)} arquivos de simulados dos exames.")

    emp_questions = []
    for f in simulados_files:
        filename = os.path.basename(f)
        exame_num = filename.split('e')[1].split('_')[0]
        with open(f, 'r', encoding='utf-8') as fp:
            items = json.load(fp)
            for item in items:
                num = item.get('num', 0)
                disc = item.get('disciplina', '')
                if 'empresarial' in disc.lower() or 'comercial' in disc.lower():
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    emp_questions.append(item)
                elif disc == '' and (exame_num == '37' and 44 <= num <= 48):
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    emp_questions.append(item)

    print(f"✅ Total de questões de Direito Empresarial extraídas: {len(emp_questions)}")

    modules = {
        '01_empresario_sociedades': {'title': 'Empresário e Sociedades Empresárias', 'questions': []},
        '02_estabelecimento_nome': {'title': 'Estabelecimento e Nome Empresarial', 'questions': []},
        '03_titulos_credito': {'title': 'Títulos de Crédito', 'questions': []},
        '04_contratos_empresariais': {'title': 'Contratos Empresariais', 'questions': []},
        '05_sociedade_anonima': {'title': 'Sociedade Anônima', 'questions': []},
        '06_falencia_recuperacao': {'title': 'Falência e Recuperação Judicial', 'questions': []},
        '07_direito_consumidor': {'title': 'Direito do Consumidor aplicado à Empresa', 'questions': []},
        '08_propriedade_intelectual': {'title': 'Propriedade Intelectual e Concorrência Desleal', 'questions': []}
    }

    for idx, q in enumerate(emp_questions, start=1):
        mod_key, mod_title = classify_emp(q)
        
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
            "fundamentacao": "<p>Código Civil de 2002 (Livro II - Do Direito de Empresa), Lei nº 6.404/1976 (S/A) e Lei nº 11.101/2005 (Recuperação e Falência).</p>",
            "dica": "<p>Examine os requisitos de caracterização do empresário, trespasse, tipos de títulos de crédito e efeitos da recuperação judicial/falência.</p>",
            "aula_comentario": f"<p>Comentário em vídeo referente ao {q.get('exame_label')}.</p>",
            "analise": f"<p>Análise detalhada das alternativas A, B, C e D em desenvolvimento.</p>"
        }

        modules[mod_key]['questions'].append(card_q)

    base_dir = '/home/sfy/Corujinha/EMPRESARIAL'
    for mod_key, data in modules.items():
        json_path = os.path.join(base_dir, f"{mod_key}_questoes.json")
        with open(json_path, 'w', encoding='utf-8') as fp:
            json.dump(data['questions'], fp, ensure_ascii=False, indent=2)
        print(f"📦 {mod_key}_questoes.json populado com {len(data['questions'])} questões.")

    print("\n🔨 Executando compilação do ecossistema Empresarial via build_emp_modules.py...")
    subprocess.run(["python3", os.path.join(base_dir, "build_emp_modules.py")], check=True)
    print("✨ Processo concluído com sucesso!")

if __name__ == '__main__':
    main()
