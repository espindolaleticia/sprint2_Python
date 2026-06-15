# =============================================================
# CHARGEGRID INTELLIGENCE — Sprint 2 — Prova de Conceito v2
# GoodWe Challenge | FIAP — Ciência da Computação | 2026.1
# =============================================================
# Grupo 2
# Integrantes:
#   Felipe Mitsuo Takahashi Stephano  — RM: 570692
#   Laura Godoy Callegari             — RM: 569181
#   Leticia Araujo Espindola          — RM: 569308
#   Mariana Dreset Carbollan          — RM: 569207
#   Milena de Aguiar Lopes Cardoso    — RM: 570599
#   Felipe Perdigão Macedo            — RM: 570990
# =============================================================

import random
import math
from datetime import datetime

# =============================================================
# CONFIGURAÇÕES DO SISTEMA
# =============================================================

LIMITE_POTENCIA_KW = 50.0
TARIFA_PICO        = 0.95   # R$/kWh — 18h–21h
TARIFA_NORMAL      = 0.55   # R$/kWh — demais horas
TARIFA_OFFPEAK     = 0.30   # R$/kWh — 00h–06h

CARREGADORES = [
    {"id": "CGR-01", "potencia_kw": 11.0, "tipo": "AC Tipo 2"},
    {"id": "CGR-02", "potencia_kw": 22.0, "tipo": "AC Tipo 2"},
    {"id": "CGR-03", "potencia_kw": 50.0, "tipo": "DC CCS"},
    {"id": "CGR-04", "potencia_kw":  7.4, "tipo": "AC Wallbox"},
]

# Histórico simulado de 24h (um valor por hora — demanda em kW)
HISTORICO_24H = [
    12.5, 8.3, 6.1, 5.0, 5.5, 7.2,   # 00h–05h (madrugada)
    14.0, 22.3, 31.5, 38.2, 40.1, 42.0,  # 06h–11h (manhã)
    44.5, 46.0, 43.2, 40.8, 39.5, 41.0,  # 12h–17h (tarde)
    52.3, 55.1, 51.8, 48.2, 38.5, 22.1   # 18h–23h (noite/pico)
]

# =============================================================
# MÓDULO 1 — TARIFAÇÃO INTELIGENTE
# =============================================================

def obter_tarifa(hora: int) -> tuple:
    if 18 <= hora <= 20:
        return TARIFA_PICO, "PICO"
    elif 0 <= hora <= 5:
        return TARIFA_OFFPEAK, "OFF-PEAK"
    else:
        return TARIFA_NORMAL, "NORMAL"


def calcular_custo(kwh: float, hora: int) -> float:
    tarifa, _ = obter_tarifa(hora)
    return round(kwh * tarifa, 2)


def melhor_horario_recarga(kwh: float) -> dict:
    """Analisa todas as 24h e recomenda o horário mais econômico."""
    melhor_hora = 0
    menor_custo = float("inf")
    for h in range(24):
        custo = calcular_custo(kwh, h)
        if custo < menor_custo:
            menor_custo = custo
            melhor_hora = h
    tarifa_atual, tipo_atual = obter_tarifa(datetime.now().hour)
    custo_atual = round(kwh * tarifa_atual, 2)
    return {
        "melhor_hora": melhor_hora,
        "menor_custo": menor_custo,
        "custo_agora": custo_atual,
        "economia": round(custo_atual - menor_custo, 2),
        "tipo_atual": tipo_atual,
    }

# =============================================================
# MÓDULO 2 — GERENCIAMENTO DE DEMANDA
# =============================================================

def simular_demanda_atual() -> list:
    estado = []
    for c in CARREGADORES:
        ativo = random.choice([True, True, False])
        consumo = round(c["potencia_kw"] * random.uniform(0.5, 1.0), 2) if ativo else 0.0
        soc = random.randint(15, 95) if ativo else 0
        estado.append({
            "id":              c["id"],
            "tipo":            c["tipo"],
            "potencia_max_kw": c["potencia_kw"],
            "consumo_kw":      consumo,
            "ativo":           ativo,
            "soc_pct":         soc,
            "throttled":       False,
        })
    return estado


def calcular_demanda_total(estado: list) -> float:
    return round(sum(c["consumo_kw"] for c in estado), 2)


def balancear_carga(estado: list, limite_kw: float) -> list:
    """
    Balanceamento inteligente com prioridade por tipo:
    DC CCS (emergência) tem prioridade máxima.
    AC são reduzidos proporcionalmente antes.
    """
    demanda = calcular_demanda_total(estado)
    if demanda <= limite_kw:
        return estado

    # Ordena: menor potência máxima = reduz primeiro (AC antes de DC)
    ajustado = sorted(estado, key=lambda x: x["potencia_max_kw"])
    excesso = round(demanda - limite_kw, 2)

    for c in ajustado:
        if not c["ativo"] or excesso <= 0:
            continue
        reducao = min(c["consumo_kw"], excesso)
        c["consumo_kw"] = round(c["consumo_kw"] - reducao, 2)
        c["throttled"] = reducao > 0
        excesso = round(excesso - reducao, 2)

    return ajustado

# =============================================================
# MÓDULO 3 — INTELIGÊNCIA ARTIFICIAL (Regressão Linear)
# =============================================================

def regressao_linear(dados: list) -> tuple:
    """
    Implementação manual de regressão linear simples (y = a + b*x).
    Encontra a tendência dos dados sem bibliotecas externas.
    Retorna (a, b) onde a = intercepto e b = coeficiente angular.
    """
    n = len(dados)
    if n < 2:
        return dados[0] if dados else 0, 0

    x = list(range(n))
    media_x = sum(x) / n
    media_y = sum(dados) / n

    numerador   = sum((x[i] - media_x) * (dados[i] - media_y) for i in range(n))
    denominador = sum((x[i] - media_x) ** 2 for i in range(n))

    b = numerador / denominador if denominador != 0 else 0
    a = media_y - b * media_x
    return round(a, 3), round(b, 3)


def prever_demanda(historico: list, passos_a_frente: int = 1) -> float:
    """
    Usa regressão linear para prever a demanda futura.
    Muito mais robusto que média ponderada — captura tendências crescentes ou decrescentes.
    """
    a, b = regressao_linear(historico)
    previsao = a + b * (len(historico) + passos_a_frente - 1)
    return round(max(0, previsao), 2)


def detectar_anomalia(historico: list, valor_atual: float) -> dict:
    """
    Detecção de anomalia por Z-score:
    Calcula o desvio padrão do histórico e verifica se o valor atual
    está além de 2 desvios padrão da média (limiar estatístico padrão).
    """
    if len(historico) < 3:
        return {"anomalia": False, "zscore": 0.0, "nivel": "normal"}

    media = sum(historico) / len(historico)
    variancia = sum((x - media) ** 2 for x in historico) / len(historico)
    desvio = math.sqrt(variancia)

    zscore = abs(valor_atual - media) / desvio if desvio > 0 else 0
    zscore = round(zscore, 2)

    if zscore > 3.0:
        nivel = "critico"
    elif zscore > 2.0:
        nivel = "alerta"
    else:
        nivel = "normal"

    return {"anomalia": zscore > 2.0, "zscore": zscore, "nivel": nivel}


def analisar_tendencia(historico: list) -> str:
    """Classifica a tendência da demanda com base no coeficiente angular."""
    _, b = regressao_linear(historico)
    if b > 1.5:
        return "CRESCIMENTO ACELERADO"
    elif b > 0.3:
        return "CRESCIMENTO MODERADO"
    elif b < -1.5:
        return "QUEDA ACELERADA"
    elif b < -0.3:
        return "QUEDA MODERADA"
    else:
        return "ESTAVEL"

# =============================================================
# MÓDULO 4 — INTEROPERABILIDADE (OCPP 1.6)
# =============================================================

def simular_mensagem_ocpp(carregador_id: str, evento: str) -> dict:
    """Simula mensagem do protocolo OCPP 1.6."""
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    mensagens = {
        "BootNotification": {
            "chargePointVendor":       "GoodWe",
            "chargePointModel":        "EV-C22",
            "chargePointSerialNumber": carregador_id,
            "firmwareVersion":         "1.4.2",
            "status":                  "Accepted",
            "currentTime":             ts,
            "interval":                300,
        },
        "MeterValues": {
            "connectorId":   1,
            "transactionId": random.randint(1000, 9999),
            "meterValue": [{
                "timestamp": ts,
                "sampledValue": [{
                    "value":     str(round(random.uniform(5.0, 22.0), 2)),
                    "measurand": "Energy.Active.Import.Register",
                    "unit":      "kWh"
                }]
            }]
        },
    }
    return {"messageType": evento, "payload": mensagens.get(evento, {})}

# =============================================================
# MÓDULO 5 — DASHBOARD TERMINAL
# =============================================================

def barra(valor: float, maximo: float, largura: int = 20, critico: float = 0.85) -> str:
    """Gera barra de progresso ASCII com indicador de nível crítico."""
    pct = min(valor / maximo, 1.0)
    preenchido = int(pct * largura)
    simbolo = "█" if pct < critico else "▓"
    return simbolo * preenchido + "░" * (largura - preenchido) + f" {pct*100:.0f}%"


def exibir_cabecalho():
    print("=" * 65)
    print("  ⚡ CHARGEGRID INTELLIGENCE v2 — Dashboard de Controle")
    print("  Sprint 2 | GoodWe Challenge | FIAP 2026.1 | Grupo 2")
    print("=" * 65)
    print(f"  Simulação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 65)


def exibir_dashboard_carregadores(estado: list, hora: int):
    tarifa, tipo = obter_tarifa(hora)
    demanda = calcular_demanda_total(estado)
    ativos = sum(1 for c in estado if c["ativo"])

    print(f"\n┌─ PAINEL DE CARREGADORES ─── {hora:02d}:00h │ Tarifa {tipo}: R${tarifa}/kWh")
    print(f"│  Demanda: {barra(demanda, LIMITE_POTENCIA_KW)} ({demanda:.1f}/{LIMITE_POTENCIA_KW:.0f} kW)")
    print(f"│  Ativos:  {ativos}/{len(estado)} carregadores")
    print("├" + "─" * 63)

    for c in estado:
        status = "●  ATIVO" if c["ativo"] else "○ INATIVO"
        throttle = " ⚠ LIMITADO" if c.get("throttled") else ""
        if c["ativo"]:
            barra_consumo = barra(c["consumo_kw"], c["potencia_max_kw"], 12)
            soc_str = f"SoC: {c['soc_pct']}%"
        else:
            barra_consumo = "░" * 12 + "   0%"
            soc_str = ""
        print(f"│  {c['id']} │ {c['tipo']:<12} │ {status:<9}{throttle}")
        if c["ativo"]:
            print(f"│         │ {barra_consumo} │ {c['consumo_kw']:.1f} kW │ {soc_str}")
    print("└" + "─" * 63)


def exibir_ia(historico: list, hora: int):
    previsao_1h = prever_demanda(historico, 1)
    previsao_3h = prever_demanda(historico, 3)
    demanda_atual = historico[-1]
    anomalia = detectar_anomalia(historico[:-1], demanda_atual)
    tendencia = analisar_tendencia(historico)
    a, b = regressao_linear(historico)

    print(f"\n┌─ INTELIGÊNCIA ARTIFICIAL ─── Regressão Linear + Z-Score")
    print(f"│  Modelo:      y = {a:.2f} + {b:.2f}x  (regressão linear simples)")
    print(f"│  Tendência:   {tendencia}")
    print(f"│  Previsão +1h: {previsao_1h:.1f} kW")
    print(f"│  Previsão +3h: {previsao_3h:.1f} kW")
    print(f"│  Anomalia (Z-score {anomalia['zscore']}): ", end="")
    if anomalia["nivel"] == "critico":
        print(f"⛔ CRÍTICO — demanda fora do padrão histórico")
    elif anomalia["nivel"] == "alerta":
        print(f"⚠️  ALERTA — desvio significativo detectado")
    else:
        print(f"✅ Normal")
    if previsao_1h > LIMITE_POTENCIA_KW * 0.85:
        print(f"│  ⚠️  Alerta preditivo: demanda prevista acima de 85% em 1h")
        print(f"│     Recomendação: redistribuir recargas para off-peak")
    print("└" + "─" * 63)


def exibir_tarifacao(hora: int):
    kwh = 30.0
    rec = melhor_horario_recarga(kwh)
    print(f"\n┌─ TARIFAÇÃO INTELIGENTE ─── {kwh:.0f} kWh de exemplo")
    print(f"│  Tarifa atual ({rec['tipo_atual']}): R$ {rec['custo_agora']:.2f}")
    print(f"│  Melhor horário:     {rec['melhor_hora']:02d}:00h → R$ {rec['menor_custo']:.2f}")
    print(f"│  Economia possível:  R$ {rec['economia']:.2f} ({rec['economia']/rec['custo_agora']*100:.0f}%)" if rec['custo_agora'] > 0 else "│  Já no melhor horário")
    print("└" + "─" * 63)


def exibir_ocpp(estado: list):
    ativo = next((c for c in estado if c["ativo"]), None)
    if not ativo:
        return
    msg = simular_mensagem_ocpp(ativo["id"], "MeterValues")
    kwh = msg["payload"]["meterValue"][0]["sampledValue"][0]["value"]
    tid = msg["payload"]["transactionId"]
    print(f"\n┌─ INTEROPERABILIDADE ─── Protocolo OCPP 1.6")
    print(f"│  Carregador:  {ativo['id']} ({ativo['tipo']}) — GoodWe EV-C22")
    print(f"│  Transação:   #{tid}")
    print(f"│  Energia:     {kwh} kWh consumidos")
    print(f"│  ✅ Mensagem padronizada OCPP — compatível com qualquer CSMS")
    print("└" + "─" * 63)


def exibir_resumo(estado: list, historico: list):
    demanda = calcular_demanda_total(estado)
    previsao = prever_demanda(historico, 1)
    hora = datetime.now().hour
    tarifa, tipo = obter_tarifa(hora)
    custo_hora = round(demanda * tarifa, 2)
    ativos = sum(1 for c in estado if c["ativo"])
    throttled = sum(1 for c in estado if c.get("throttled"))

    print(f"\n{'='*65}")
    print(f"  RESUMO EXECUTIVO")
    print(f"{'='*65}")
    print(f"  Demanda atual:    {demanda:.1f} kW / {LIMITE_POTENCIA_KW:.0f} kW ({demanda/LIMITE_POTENCIA_KW*100:.0f}%)")
    print(f"  Carregadores:     {ativos} ativos | {throttled} limitados")
    print(f"  Custo estimado:   R$ {custo_hora:.2f}/hora ({tipo})")
    print(f"  Previsão 1h:      {previsao:.1f} kW")
    status_geral = "✅ SISTEMA ESTÁVEL" if demanda <= LIMITE_POTENCIA_KW else "⚠️  SOBRECARGA DETECTADA"
    print(f"  Status:           {status_geral}")
    print(f"{'='*65}")
    print(f"  ChargeGrid Intelligence v2 | Grupo 2 | FIAP 2026.1")
    print(f"{'='*65}\n")

# =============================================================
# EXECUÇÃO PRINCIPAL
# =============================================================

def main():
    exibir_cabecalho()

    hora = datetime.now().hour
    estado = simular_demanda_atual()
    demanda_antes = calcular_demanda_total(estado)

    # Balanceamento de carga
    estado = balancear_carga(estado, LIMITE_POTENCIA_KW)

    # Usa histórico real de 24h + valor atual simulado
    historico = HISTORICO_24H.copy()
    historico.append(demanda_antes)

    exibir_dashboard_carregadores(estado, hora)
    exibir_ia(historico, hora)
    exibir_tarifacao(hora)
    exibir_ocpp(estado)
    exibir_resumo(estado, historico)


if __name__ == "__main__":
    main()
