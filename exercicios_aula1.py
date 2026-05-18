import itertools
import random
import time
from typing import Dict, List, Optional, Tuple

TAREFAS = [
    {"nome": "Auth OAuth2",          "custo": 8,  "valor": 40},  # 0
    {"nome": "Dashboard métricas",   "custo": 13, "valor": 55},  # 1
    {"nome": "Exportar CSV",         "custo": 5,  "valor": 20},  # 2
    {"nome": "Refactor serviço X",   "custo": 20, "valor": 35},  # 3
    {"nome": "API notificações",     "custo": 10, "valor": 60},  # 4
    {"nome": "Upgrade deps",         "custo": 3,  "valor": 15},  # 5
    {"nome": "Testes E2E checkout",  "custo": 8,  "valor": 50},  # 6
    {"nome": "Rate limiting",        "custo": 6,  "valor": 45},  # 7
    {"nome": "Docs OpenAPI",         "custo": 4,  "valor": 25},  # 8
    {"nome": "Cache Redis",          "custo": 12, "valor": 70},  # 9
]

CAPACIDADE = 40  # Story Points máximos na Sprint

def avaliar_solucao(individuo: List[int], tarefas: List[Dict], capacidade: int) -> int:
    #Retorna o valor total da solução ou 0 se ultrapassar a capacidade
    custo_total = sum(tarefas[i]["custo"] for i in range(len(tarefas)) if individuo[i] == 1)
    if custo_total > capacidade:
        return 0
    return sum(tarefas[i]["valor"] for i in range(len(tarefas)) if individuo[i] == 1)


def exibir_solucao(individuo: List[int], tarefas: List[Dict], titulo: str = "") -> None:
    #Imprime as tarefas selecionada, custo e valor total
    if titulo:
        print(f"\n{'='*55}")
        print(f"  {titulo}")
        print(f"{'='*55}")

    selecionadas = [tarefas[i] for i in range(len(tarefas)) if individuo[i] == 1]
    custo_total  = sum(t["custo"] for t in selecionadas)
    valor_total  = sum(t["valor"] for t in selecionadas)

    print(f"  {'Tarefa':<25} {'Custo':>6} {'Valor':>6}")
    print(f"  {'-'*40}")
    for t in selecionadas:
        print(f"  {t['nome']:<25} {t['custo']:>6} {t['valor']:>6}")
    print(f"  {'-'*40}")
    print(f"  {'TOTAL':<25} {custo_total:>6} {valor_total:>6}")
    print(f"  Capacidade usada: {custo_total}/{CAPACIDADE} SP")


# Exercício 1 — Busca Exaustiva (Brute Force)   O(2^n)
def busca_exaustiva(
    tarefas: List[Dict],
    capacidade: int
) -> Tuple[List[int], int]:
    #Encontra a Sprint ótima testando todas as combinações
    n = len(tarefas)
    melhor_individuo = [0] * n
    melhor_valor = 0

    for combo in itertools.product([0, 1], repeat=n):
        individuo = list(combo)

        custo_total = sum(tarefas[i]["custo"] for i in range(n) if individuo[i] == 1)
        if custo_total > capacidade:
            continue  # combinação inválida — ultrapassa a capacidade

        valor_total = sum(tarefas[i]["valor"] for i in range(n) if individuo[i] == 1)
        if valor_total > melhor_valor:
            melhor_valor = valor_total
            melhor_individuo = individuo

    return melhor_individuo, melhor_valor

# Exercício 2 — Heurística Gulosa (Greedy)   O(n log n)
def greedy_knapsack(
    tarefas: List[Dict],
    capacidade: int
) -> Tuple[List[int], int]:
    # Ordena por ROI decrescente e adiciona tarefas. ROI = valor / custo  (valor por Story Point).
    n = len(tarefas)
    individuo = [0] * n
    capacidade_restante = capacidade

    # Preserva o índice original para marcar corretamente o indivíduo.
    indices = sorted(
        range(n),
        key=lambda i: tarefas[i]["valor"] / tarefas[i]["custo"],
        reverse=True,
    )

    for i in indices:
        if tarefas[i]["custo"] <= capacidade_restante:
            individuo[i] = 1
            capacidade_restante -= tarefas[i]["custo"]

    valor_total = sum(tarefas[i]["valor"] for i in range(n) if individuo[i] == 1)
    return individuo, valor_total


# Exercício 3 — Análise Empírica de Complexidade
def medir_complexidade(
    tamanhos: List[int],
    capacidade: int = 30,
    repeticoes: int = 3,
) -> Dict[int, float]:
    """Mede o tempo médio do brute force para diferentes n."""
    resultados = {}
    for n in tamanhos:
        tempos = []
        for _ in range(repeticoes):
            tarefas_rand = [
                {"custo": random.randint(1, 10), "valor": random.randint(5, 50)}
                for _ in range(n)
            ]
            # TODO (Ex 3): medir tempo com time.perf_counter()
            pass
        # TODO (Ex 3): resultados[n] = média dos tempos em ms
        pass
    return resultados


def calcular_razoes_crescimento(tempos: Dict[int, float]) -> None:
    """Imprime tabela de tempos e razões de crescimento."""
    ns = sorted(tempos.keys())
    # TODO (Ex 3): imprimir n | Tempo (ms) | Razão | 2^n
    pass


# Exercício 4 — Hill Climbing

def gerar_vizinhos(individuo: List[int]) -> List[List[int]]:
    """Gera todos os n vizinhos (soluções a 1 bit de distância)."""
    # TODO (Ex 4)
    pass


def hill_climbing(
    tarefas: List[Dict],
    capacidade: int,
    solucao_inicial: Optional[List[int]] = None,
    max_iter: int = 1000,
    verbose: bool = False,
) -> Tuple[List[int], int, int]:
    """Busca local: melhora iterativamente trocando 1 bit por vez.

    Retorna: (melhor_individuo, melhor_valor, n_iteracoes)
    """
    if solucao_inicial is None:
        atual, _ = greedy_knapsack(tarefas, capacidade)
    else:
        atual = solucao_inicial[:]

    atual_valor = avaliar_solucao(atual, tarefas, capacidade)
    n_iter = 0
    # TODO (Ex 4): implementar o loop de hill climbing
    pass
    return atual, atual_valor, n_iter


# Comparação e testes

def comparar_abordagens(tarefas: List[Dict], capacidade: int) -> None:
    #Executa e compara Brute Force vs Greedy vs Análise Empírica de Complexidade vs Hill Climbing para o conjunto completo
    print("\n" + "#" * 60)
    print("#  COMPARAÇÃO DAS ABORDAGENS")
    print("#" * 60)

    # --- Brute Force ---
    t0 = time.perf_counter()
    ind_bf, val_bf = busca_exaustiva(tarefas, capacidade)
    tempo_bf = (time.perf_counter() - t0) * 1000
    exibir_solucao(ind_bf, tarefas, f"Ex 1 — Brute Force  ({tempo_bf:.1f} ms)")

    # --- Greedy ---
    t0 = time.perf_counter()
    ind_gr, val_gr = greedy_knapsack(tarefas, capacidade)
    tempo_gr = (time.perf_counter() - t0) * 1000
    exibir_solucao(ind_gr, tarefas, f"Ex 2 — Greedy  ({tempo_gr:.3f} ms)")

    # --- Resumo ---
    diff = val_bf - val_gr
    otimo_gr = "Sim" if val_gr == val_bf else "Não"
 
    col_abord  = f"{'Abordagem':<18}"
    col_compl  = f"{'Complexidade':^14}"
    col_valor  = f"{'Valor':>6}"
    col_tempo  = f"{'Tempo':>10}"
    col_otimo  = f"{'Ótimo?':^9}"
    col_escala = f"{'Escala?':^9}"
    col_prat   = f"{'Prático?':^20}"
 
    sep = "  " + "-" * 96
 
    print(f"\n{'='*98}")
    print(f"  Resumo das abordagens")
    print(f"{'='*98}")
    print(f"  {col_abord}  {col_compl}  {col_valor}  {col_tempo}  {col_otimo}  {col_escala}  {col_prat}")
    print(sep)
    print(
        f"  {'Brute Force':<18}  {'O(2ⁿ)':^14}  {val_bf:>6}  {tempo_bf:>8.1f}ms"
        f"  {'Sim':^9}  {'Não':^9}  {'Inviável n>25':^20}"
    )
    print(
        f"  {'Greedy':<18}  {'O(n log n)':^14}  {val_gr:>6}  {tempo_gr:>8.3f}ms"
        f"  {otimo_gr:^9}  {'Sim':^9}  {'Sub-ótimo':^20}"
    )
 
 
def _assert_ex1() -> None:
    #Verifica que a busca exaustiva encontra o ótimo conhecido
    ind, val = busca_exaustiva(TAREFAS, CAPACIDADE)
    custo = sum(TAREFAS[i]["custo"] for i in range(len(TAREFAS)) if ind[i] == 1)
    assert custo <= CAPACIDADE, "Capacidade ultrapassada no Ex 1!"
    assert val > 0, "Valor zero no Ex 1!"
    print(f"Ex 1 OK — valor={val}, custo={custo}")
 
 
def _assert_ex2() -> None:
    #Verifica que o greedy respeita a capacidade e produz valor positivo
    ind, val = greedy_knapsack(TAREFAS, CAPACIDADE)
    custo = sum(TAREFAS[i]["custo"] for i in range(len(TAREFAS)) if ind[i] == 1)
    assert custo <= CAPACIDADE, "Capacidade ultrapassada no Ex 2!"
    assert val > 0, "Valor zero no Ex 2!"
    print(f"Ex 2 OK — valor={val}, custo={custo}")
 
 
# Entry point
if __name__ == "__main__":
    print("Teoria da Computação — Sprint Planning como Knapsack")
    print(f"Tarefas disponíveis: {len(TAREFAS)} | Capacidade: {CAPACIDADE} SP\n")
 
    _assert_ex1()
    _assert_ex2()
 
    comparar_abordagens(TAREFAS, CAPACIDADE)