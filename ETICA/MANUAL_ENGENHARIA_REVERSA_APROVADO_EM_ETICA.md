# 📘 MANUAL DE ENGENHARIA REVERSA & BLUEPRINT ARQUITETURAL
## PROJETO: PLATAFORMA "APROVADO EM ÉTICA" (OAB 1ª FASE)

> **Documentação de Especificação Técnica e Pedagógica de Alta Fidelidade**  
> *Versão:* 2.0 | *Data:* Setembro de 2026  
> *Objetivo:* Permitir a reconstrução, replicação e expansão integral do projeto por qualquer agente de Inteligência Artificial ou equipe de engenharia de software, garantindo 100% de paridade técnica, visual e pedagógica.

---

## 1. VISÃO GERAL E PROPÓSITO DO SISTEMA

O **Aprovado em Ética** é uma aplicação web moderna (Single-Page Application - SPA responsiva), desenvolvida sob o padrão **Clean Premium**, dedicada ao ensino ativo e à preparação de candidatos para a prova de Ética Profissional do Exame de Ordem da OAB (Estatuto da OAB - Lei 8.906/94, Regulamento Geral e Código de Ética e Disciplina - CED).

### 🎯 Pilares Estratégicos:
1. **Transparência Pedagógica ("No-Invented-Content"):** Todo o conteúdo doutrinário e os comentários são estritamente fiéis às transcrições literais do curso preparatório da Profª. Maria Christina (Gran Cursos OAB - 8 episódios).
2. **Integração Forense de Exames (Jurimetria OAB):** Adoção de um acervo histórico real com **193 questões únicas e auditadas dos Exames 37 ao 46 da FGV**, acompanhadas de simulação temática sem sobreposição.
3. **Estudo Ativo Dual:** Unificação, no mesmo card de módulo, de acesso imediato ao **Resumo Esquemático da Aula** e ao **Simulado de Questões com Flip-Cards 3D**.
4. **Design System Premium Sobriety:** Paleta de cores sofisticada baseada em Tons de Preto/Grafite (`#0f172a`), Amarelo/Âmbar (`#f59e0b`), Fundo Claro Limpo (`#f8fafc`), tipografia Inter/Google Fonts e microinterações fluidas.

---

## 2. ARQUITETURA DE DIRETÓRIOS E COMPONENTES

A estrutura de arquivos localiza-se no diretório raiz do módulo: `/home/sfy/Corujinha/ETICA/`

```
/home/sfy/Corujinha/ETICA/
├── 📄 MANUAL_ENGENHARIA_REVERSA_APROVADO_EM_ETICA.md   # (Este documento)
├── ⚙️ build_all_modules.py                             # Motor central de compilação dos HTMLs
├── 🖥️ Dashboard_Etica_Premium.html                      # Hub principal da aplicação
├── 🖥️ Etica_01_Orgaos_da_OAB_Premium.html               # SPA Módulo 01
├── 🖥️ Etica_02_Direitos_e_Prerrogativas_Premium.html    # SPA Módulo 02
├── 🖥️ Etica_03_Incompatibilidade_e_Impedimento_Premium.html # SPA Módulo 03
├── 🖥️ Etica_04_Infracoes_e_Sancoes_Premium.html         # SPA Módulo 04
├── 🖥️ Etica_05_Publicidade_e_Honorarios_Premium.html    # SPA Módulo 05
├── 🖥️ Etica_06_Publicidade_e_Marketing_Premium.html     # SPA Módulo 06
├── 🖥️ Etica_07_Advogados_e_Estagiarios_Premium.html    # SPA Módulo 07
├── 🖥️ Etica_08_Processo_Administrativo_e_Eleitoral_Premium.html # SPA Módulo 08
├── 🖥️ Etica_RetaFinal_Premium.html                     # SPA Simulado Reta Final OAB 47
│
├── 📂 DATASETS E TRANSCRIÇÕES POR MÓDULO (01 a 08):
│   ├── 0X_nome_modulo.pt.vtt                           # Arquivo de legenda/áudio original
│   ├── 0X_nome_modulo_transcricao.md                   # Transcrição literal sanitizada
│   ├── 0X_nome_modulo_resumo.md                        # Resumo teórico esquemático em Markdown
│   └── 0X_nome_modulo_questoes.json                    # Dataset de questões estruturado
```

---

## 3. ESPECIFICAÇÃO DE MÓDULOS E CONTEÚDO

O curso divide-se rigorosamente em **8 Módulos Temáticos**, correspondentes aos 8 episódios da matriz da Profª. Maria Christina:

| Módulo | Slug do Arquivo | Nome Oficial do Módulo | Foco Normativo Principal |
|:---:|---|---|---|
| **01** | `01_orgaos_da_oab` | Órgãos da OAB | Arts. 44 a 55 do EAOAB (CFOAB, Seccionais, Subseções, CAA) |
| **02** | `02_direitos_e_prerrogativas` | Direitos e Prerrogativas do Advogado | Arts. 6º a 7º-B do EAOAB (Sigilo, Inviolabilidade, Prisão, Lei Júlia Matos) |
| **03** | `03_incompatibilidade_e_impedimento` | Incompatividades e Impedimentos | Arts. 27 a 30 do EAOAB (Proibições totais e parciais) |
| **04** | `04_infracoes_e_sancoes` | Infrações e Sanções Disciplinares | Arts. 34 a 43 do EAOAB (Censura, Suspensão, Exclusão, Multa, Prescrição) |
| **05** | `05_publicidade_e_honorarios` | Sociedades de Advogados e Honorários | Arts. 15 a 17, 22 a 26 do EAOAB (Sociedade Simples, SUA, Sucumbência) |
| **06** | `06_publicidade_e_marketing` | Publicidade e Marketing Jurídico | Provimento 205/2021 CFOAB e Arts. 39 a 47 do CED (Redes sociais, captação) |
| **07** | `07_advogados_e_estagiarios` | Advogados, Estagiários e Atos Privativos | Arts. 1º a 5º, 8º a 14 do EAOAB (Inscrição, Bacharel, Estágio, Procuração) |
| **08** | `08_processo_administrativo_e_eleitoral` | Processo Eleitoral e Processo Disciplinar | Arts. 63 a 77 do EAOAB (Eleições OAB, Rito do PAD, Recursos) |

---

## 4. SCHEMA DOS DATASETS DE QUESTÕES (`0X_..._questoes.json`)

Cada arquivo `.json` de questões deve conter um array de objetos obedecendo estritamente ao seguinte esquema JSON:

```json
{
  "num": 1,
  "id": 1,
  "exame": "46º Exame OAB",
  "tema": "Direitos da Advogada Gestante (Art. 7º-A, EAOAB) - Exame 46",
  "enunciado": "<p>Paloma, advogada gestante, compareceu ao Fórum...</p>",
  "opcoes": {
    "A": "Texto da alternativa A...",
    "B": "Texto da alternativa B...",
    "C": "Texto da alternativa C...",
    "D": "Texto da alternativa D..."
  },
  "gabarito": "C",
  "core": true,
  "sintese": "<p>Direitos Específicos da Advogada Gestante e Lactante (Lei Júlia Matos)</p>",
  "logica_conceito": "<p><b>Por que a lei é assim?</b> A Lei 13.363/2016 garante proteção à maternidade...</p>",
  "fundamentacao": "<p>Art. 7º-A, inciso I, alínea 'b' da Lei nº 8.906/94 (EAOAB)...</p>",
  "dica": "<p>Lembre-se do rol do Art. 7º-A do EAOAB: Gestante tem direito a não passar por detector de metais!</p>",
  "aula_comentario": "<p><i>'A Lei Júlia Matos garante prerrogativas fundamentais para a advogada gestante... Gabarito Letra C.'</i> — Profª. Maria Christina</p>",
  "analise": "<p><b>C) Correta:</b> Aplicação direta do Art. 7º-A do EAOAB.<br><b>A, B, D) Incorretas:</b> Fundamentos de rejeição das demais opções.</p>"
}
```

### 📌 Regras de Validação do Schema:
- **`exame`**: Deve indicar expressamente a prova de origem (ex: `"37º Exame OAB"` a `"46º Exame OAB"` ou `"Simulado Didático OAB"`).
- **`enunciado`**: Deve vir encapsulado em `<p>...</p>`.
- **`aula_comentario`**: Deve reproduzir fielmente a fala e lição da Profª. Maria Christina para a questão.
- **`analise`**: Deve cobrir a justificativa da alternativa **Correta** e a refutação detalhada de cada alternativa **Incorreta**.

---

## 5. DESIGN SYSTEM & IDENTIDADE VISUAL PREMIUM

### 🎨 Tabela de Tokens de Cores (CSS Variables):

```css
:root {
  /* Cores Principais */
  --bg-main: #f8fafc;
  --surface: #ffffff;
  --surface-border: #e2e8f0;
  
  /* Tipografia Profunda */
  --text-dark: #0f172a;
  --text-medium: #334155;
  --text-light: #64748b;
  
  /* Âmbar / Amarelo Premium (Destaques e Etiquetas) */
  --amber-primary: #f59e0b;
  --amber-dark: #b45309;
  --amber-light: #fffbeb;
  --amber-border: #fde68a;
  
  /* Botões e Ações */
  --btn-primary-bg: #0f172a;
  --btn-primary-hover: #1e293b;
  --btn-secondary-bg: #f1f5f9;
  --btn-secondary-hover: #e2e8f0;
  
  /* Feedback e Status */
  --success: #10b981;
  --danger: #ef4444;
}
```

### 📐 Diretrizes de Componentes Visuais:

1. **Cabeçalho Global da Aplicação:**
   - Canto Superior Esquerdo:
     - Marca / Ícone: `OAB` em pill amarela/escura.
     - Título: `Ética Profissional`.
     - Subtítulo / Usuário: `André L. da Silva`.
   - Canto Superior Direito:
     - Botão / Pill: `8 Módulos Concluídos` e `Exame de Ordem 47`.
   - Botão de Retorno Global:
     - Ícone `←` fixo na extremidade esquerda da barra superior em todas as telas de módulo (`Etica_0X_...html`), retornando diretamente ao `Dashboard_Etica_Premium.html`.

2. **Cards de Módulos (Dashboard):**
   - Design retangular soberbo com bordas suavizadas (`border-radius: 12px`).
   - Rodapé com **2 botões dispostos simetricamente (50% / 50%)**:
     - Botão 1 (Esquerda): `Resumo Aula` (Fundo cinza claro `#f1f5f9`, contorno `#cbd5e1`, ícone de livro). Abre a SPA posicionada na aba de teoria (`#resumo`).
     - Botão 2 (Direita): `Questões` (Fundo sólido escuro `#0f172a`, texto branco, ícone de seta). Abre a SPA no simulado interativo (`#quiz`).

3. **Interface do Simulado (Card Flip 3D):**
   - **Cabeçalho do Slide:**
     - Número da questão (ex: `Q1 / 45`).
     - **Etiqueta do Exame (Badge Âmbar):** `<span class="q-exame-badge">⭐ 46º Exame OAB</span>`.
     - Nome do Subtema.
     - Temporizador Regressivo de 45 segundos com barra de progresso animada.
   - **Face Frontal (Pergunta):** Enunciado e opções com efeito hover.
   - **Face Traseira (Gabarito & Didática):** Ativada ao responder. Exibe a explicação da professora, lógica do conceito, síntese, fundamentação legal e análise detalhada.

---

## 6. SCRIPT DE COMPILAÇÃO AUTOMATIZADA (`build_all_modules.py`)

A geração das páginas HTML da plataforma é 100% automatizada através do script Python `/home/sfy/Corujinha/ETICA/build_all_modules.py`.

### 🔄 Fluxo de Compilação:
1. **Varredura:** O script lê o diretório `/home/sfy/Corujinha/ETICA/` em busca dos pares `0X_..._resumo.md` e `0X_..._questoes.json`.
2. **Parsing Markdown:** Converte a teoria da aula para blocos HTML formatados com caixas didáticas (`box-law`, `box-warning`, `box-tip`).
3. **Parsing JSON:** Injeta as questões e metadados no componente Javascript da SPA.
4. **Template HTML Engine:** Concatena os estilos CSS incorporados, a estrutura DOM responsiva e o código de animação/persistência JS (`localStorage`).
5. **Output:** Escreve os arquivos estáticos `Etica_0X_..._Premium.html` e `Etica_RetaFinal_Premium.html`.

---

## 7. PROTOCOLO DE INGESTÃO E DEDUPLICAÇÃO DE EXAMES (JURIMETRIA)

Para escalar o acervo de questões sem comprometer a integridade do banco de dados, deve-se seguir este protocolo:

1. **Fonte de Dados:** Ler os arquivos Markdown de exames anteriores localizados no repositório local `/home/sfy/Jurimetria_OAB/QST_Questoes/exame_XX/`.
2. **Classificação Temática:** Mapear o `subtema` oficial para o módulo correspondente (01 a 08).
3. **Enriquecimento Pedagógico:** Adicionar obrigatoriamente os 8 campos pedagógicos (`sintese`, `logica_conceito`, `fundamentacao`, `dica`, `aula_comentario`, `analise`, `exame`, `tema`).
4. **Deduplicação Programática (Sanitização):**
   - Aplicar normalização de texto aos enunciados (remover tags HTML, pontuação e converter para caixa baixa).
   - Verificar correspondência exata ou de prefixo (primeiros 60 caracteres).
   - Rejeitar inserções duplicadas, garantindo que o acervo permaneça **100% único**.
5. **Recompilação:** Executar `python3 build_all_modules.py` para reconstruir a interface.

---

## 8. PROMPT DE REPLICAÇÃO PARA AGENTES DE IA (SAFE-TO-REPLICATE)

Se for necessário recriar o projeto do zero usando qualquer modelo de IA, forneça as seguintes instruções em lote:

```text
Você é o assistente técnico encarregado de reconstruir a plataforma "Aprovado em Ética OAB".
Siga rigorosamente estas especificações:
1. Acesse o repositório em /home/sfy/Corujinha/ETICA/ e leia MANUAL_ENGENHARIA_REVERSA_APROVADO_EM_ETICA.md.
2. Certifique-se de que os 8 módulos possuem transcrições literais (.md) extraídas dos 8 vídeos da Profª. Maria Christina (Gran Cursos OAB).
3. Garanta que a paleta de cores siga o padrão Clean Premium (Preto #0f172a, Grafite, Âmbar #f59e0b, Fundo #f8fafc).
4. No Dashboard_Etica_Premium.html, formate o cabeçalho com o nome do usuário 'André L. da Silva', a disciplina 'Ética Profissional', e disponha 2 botões simétricos (50%/50%) no rodapé de cada card: 'Resumo Aula' e 'Questões'.
5. Certifique-se de que em todas as páginas HTML de módulo haja o botão universal de retorno (←) para a Home.
6. Mantenha os datasets JSON enriquecidos com os 8 campos didáticos e a etiqueta de exame (ex: '⭐ 46º Exame OAB').
7. Execute o script build_all_modules.py para compilar a plataforma final com zero duplicidades.
```

---

## 9. FRAMEWORK DE EXPANSÃO MULTI-DISCIPLINAR (QUALQUER MATÉRIA DA OAB)

Esta arquitetura foi projetada como um **pipeline genérico e parametrizável**. Para aplicar este mesmo modelo industrial a qualquer nova disciplina do Exame de Ordem (ex: *Direito Constitucional, Direito Penal, Direito Civil, Processo Penal, etc.*), siga a esteira de 5 passos:

```
[Playlist YouTube de Aulas] ──► [Transcrição .vtt] ──► [Resumo Teórico .md] ──┐
                                                                              ├──► [Pipeline Python] ──► [SPA HTML Premium]
[Cadernos Jurimetria_OAB]  ──► [Filtro Matéria]   ──► [Enriquecimento JSON] ──┘
```

### 📋 Esteira de Execução para Novas Disciplinas:

1. **Ingestão de Aulas (Transcrições Literais):**
   - Baixar arquivos `.pt.vtt` da playlist da nova disciplina.
   - Gerar `XX_nome_modulo_transcricao.md` sanitizando timestamps.
   - Extrair `XX_nome_modulo_resumo.md` em formato esquemático (*No-Invented-Content*).

2. **Ingestão de Questões Históricas (`Jurimetria_OAB`):**
   - Filtrar o repositório de provas (Exames 37 ao 46+) pela disciplina-alvo.
   - Agrupar questões por subtemas da nova matéria.

3. **Padronização do Dataset JSON:**
   - Preencher os 8 campos pedagógicos mandatórios (`sintese`, `logica_conceito`, `fundamentacao`, `dica`, `aula_comentario`, `analise`, `exame`, `tema`).
   - Aplicar a trava de deduplicação por hash/prefixo de enunciado.

4. **Compilação Estática (Build Engine):**
   - Adaptar o script `build_all_modules.py` apontando para o diretório da nova matéria.
   - Manter os tokens visuais **Clean Premium** (Fundo `#f8fafc`, Preto `#0f172a`, Âmbar `#f59e0b`).
   - Renderizar o rodapé dual com botões simétricos (50%/50%): `Resumo Aula` e `Questões`.

5. **Validação de Cobertura e Navegação:**
   - Garantir a presença do botão de retorno `←` em todas as telas apontando para o Dashboard da disciplina.

---
*Manual homologado e finalizado para a arquitetura multi-disciplinar da plataforma.*

