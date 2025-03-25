from ortools.linear_solver import pywraplp

def productionPlanningProblem():
    solver = pywraplp.Solver.CreateSolver("GLOP")  # GLOP = Solver de Programação Linear

    if not solver:
        print('Solver não pode ser criado.')
        return

    # Parâmetros do problema
    e_initial = 5000  # Estoque inicial
    t = 4  # t representa os próximos quatro meses
    demand = [7000, 15000, 10000, 8000]  # Demanda mensal
    production_capacity = 10000  # Capacidade de produção regular
    overtime_capacity = 2500  # Capacidade de produção em hora extra
    cost_xt = 2000  # Custo de produção regular (xt)
    cost_yt = 2200  # Custo de produção em hora extra (yt)
    cost_et = 100  # Custo de armazenamento (et)
    
    # Variáveis de decisão
    xt = [solver.NumVar(0, production_capacity, f"x_{i}") for i in range(t)]  # xt: produção regular
    yt = [solver.NumVar(0, overtime_capacity, f"y_{i}") for i in range(t)]  # yt: produção em hora extra
    et = [solver.NumVar(0, solver.infinity(), f"e_{i}") for i in range(t)]  # et: estoque ao final do mês

    # Restrições de balanço de estoque
    solver.Add(xt[0] + yt[0] - et[0] == demand[0] - e_initial)  # Primeiro mês
    for i in range(1, t):
        solver.Add(et[i-1] + xt[i] + yt[i] - et[i] == demand[i])  # Meses subsequentes

    # Função objetivo (minimizar custos)
    total_cost = solver.Sum([
        cost_xt * xt[i] + cost_yt * yt[i] + cost_et * et[i]
        for i in range(t)
    ])
    solver.Minimize(total_cost)

    # Resolver o problema
    status = solver.Solve()

    # Exibir resultados
    print("Dados do problema:")
    print("Número de variáveis =", solver.NumVariables())
    if status == pywraplp.Solver.OPTIMAL:
        print("Solução ótima encontrada!\n")
        for i in range(t):
            print(f"Mês {i+1}:")
            print(f"  xt (Produção regular): {xt[i].solution_value()}")
            print(f"  yt (Produção em hora extra): {yt[i].solution_value()}")
            print(f"  et (Estoque ao final): {et[i].solution_value()}")
            print(f"  Custo de armazenamento: {cost_et * et[i].solution_value()}\n")
        print(f"Custo total: {solver.Objective().Value()}")
    else:
        print("Nenhuma solução ótima encontrada.")   

productionPlanningProblem()