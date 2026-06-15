# ChargeGrid Intelligence – Sprint 2

## GoodWe Challenge | FIAP – Ciência da Computação | 2026.1

### Integrantes

* Felipe Mitsuo Takahashi Stephano – RM 570692 – 1CCPJ
* Laura Godoy Callegari – RM 569181 – 1CCPJ
* Leticia Araujo Espindola – RM 569308 – 1CCPJ
* Mariana Dreset Carbollan – RM 569207 – 1CCPJ
* Milena de Aguiar Lopes Cardoso – RM 570599 – 1CCPJ

---

# 1. Descrição da Solução

O ChargeGrid Intelligence é uma prova de conceito desenvolvida para simular o gerenciamento inteligente de estações de recarga para veículos elétricos em ambientes comerciais.

O sistema foi construído com base nos quatro pilares definidos na Sprint 1: controle de demanda, tarifação dinâmica, interoperabilidade e inteligência artificial. A proposta é demonstrar como diferentes carregadores podem operar de forma integrada, permitindo o monitoramento do consumo energético, a distribuição equilibrada da carga elétrica e a previsão de demanda futura.

A solução foi implementada em Python e executada em ambiente local, sem necessidade de bibliotecas externas.

---

# 2. Evolução da Sprint 1 para a Sprint 2

Na Sprint 1 foi realizada a análise dos principais desafios relacionados à infraestrutura de recarga de veículos elétricos, bem como o estudo dos quatro pilares do projeto.

Na Sprint 2 esses conceitos foram transformados em uma solução funcional, permitindo a simulação dos processos de monitoramento, controle de carga, tarifação e previsão de demanda.

Principais avanços:

* Implementação prática dos quatro pilares em Python;
* Simulação de múltiplos carregadores funcionando simultaneamente;
* Aplicação de regras de balanceamento de carga;
* Cálculo automático de tarifas conforme o horário;
* Geração de previsões de demanda utilizando dados históricos;
* Simulação de comunicação baseada no protocolo OCPP 1.6.

---

# 3. Arquitetura do Sistema

O sistema é composto por carregadores conectados a um barramento central, responsável por enviar informações ao motor de gestão inteligente.

Esse motor realiza as seguintes funções:

* Monitoramento da demanda energética;
* Balanceamento de carga;
* Aplicação das tarifas de energia;
* Registro do histórico de consumo;
* Previsão de demanda futura;
* Simulação da comunicação via protocolo OCPP.

Fluxo simplificado do sistema:

Leitura dos carregadores

↓

Cálculo da demanda total

↓

Verificação do limite de capacidade

↓

Balanceamento automático da carga (quando necessário)

↓

Aplicação da tarifa correspondente ao horário

↓

Registro do histórico

↓

Previsão da próxima demanda

↓

Geração de alertas e relatório final

---

# 4. Funcionalidades Implementadas

## 4.1 Gerenciamento Inteligente de Demanda

* Monitoramento simultâneo de carregadores AC e DC;
* Detecção automática de sobrecarga;
* Redistribuição da potência disponível;
* Priorização dos carregadores de corrente contínua em situações críticas.

## 4.2 Tarifação Dinâmica

O sistema aplica diferentes valores de cobrança conforme o horário de utilização.

Faixas tarifárias:

* Horário de pico (18h às 21h): R$ 0,95/kWh
* Horário normal: R$ 0,55/kWh
* Horário fora de pico (0h às 6h): R$ 0,30/kWh

Além do cálculo do valor da recarga, o sistema também demonstra possíveis economias obtidas ao utilizar períodos de menor demanda.

## 4.3 Previsão de Demanda

Foi implementado um modelo simples de previsão baseado em média ponderada do histórico de consumo.

As leituras mais recentes recebem maior peso, permitindo estimativas mais próximas da realidade operacional.

Quando a previsão ultrapassa 85% da capacidade disponível, o sistema gera alertas preventivos.

## 4.4 Interoperabilidade

A solução simula mensagens inspiradas no protocolo OCPP 1.6, amplamente utilizado em estações de recarga.

Entre as mensagens simuladas estão:

* BootNotification
* StatusNotification
* MeterValues

Essa abordagem demonstra a possibilidade de integração entre equipamentos de diferentes fabricantes.

---

# 5. Estrutura do Projeto

chargegrid-sprint2/

├── chargegrid_poc_v2.py

└── README.md

Descrição dos arquivos:

* chargegrid_poc_v2.py: código principal da prova de conceito.
* README.md: documentação do projeto.

---

# 6. Instruções de Execução

Pré-requisitos:

* Python 3.10 ou superior.

Execução:

python chargegrid_poc_v2.py

Não é necessária a instalação de bibliotecas adicionais.

---

# 7. Materiais Técnicos Utilizados

* Linguagem Python 3.10+
* Conceitos de Smart Grid
* Gerenciamento de demanda elétrica
* Tarifação dinâmica de energia
* Protocolo OCPP 1.6
* Média ponderada para previsão de demanda
* Estruturas de dados e lógica de programação

---

# 8. Considerações Finais

O desenvolvimento do ChargeGrid Intelligence permitiu aplicar conceitos estudados durante a disciplina em um cenário próximo ao encontrado em sistemas reais de recarga de veículos elétricos.

A implementação dos quatro pilares propostos demonstrou a viabilidade de soluções inteligentes para monitoramento, distribuição de carga, cobrança de energia e previsão de consumo. Além disso, o projeto proporcionou experiência prática no desenvolvimento de sistemas em Python e na modelagem de processos voltados à gestão energética.
