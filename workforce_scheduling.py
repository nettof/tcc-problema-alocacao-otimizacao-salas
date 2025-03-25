from ortools.linear_solver import pywraplp

def wworkforce_scheduling():    
    solver = pywraplp.Solver.CreateSolver('SCIP')

    if not solver:
        print('Solver não pode ser criado.')
        return

    # Parâmetros
    days = 7
    demand = [14, 13, 15, 16, 19, 18, 11]

    # Variáveis de decisão: x[i] = número de trabalhadores que começam no dia i
    x = []
    for i in range(days):
        x.append(solver.IntVar(0, solver.infinity(), f'x[{i+1}]'))

    # Restrições: garantir que a demanda de cada dia seja atendida
    for d in range(days):
        # Trabalhadores que cobrem o dia d (dias consecutivos de trabalho)
        solver.Add(
            x[d % days] + x[(d - 1) % days] + x[(d - 2) % days] + x[(d - 3) % days] + x[(d - 4) % days] >= demand[d],
            f'Demanda_dia_{d+1}'
        )

    # Função objetivo
    solver.Minimize(solver.Sum(x))

    status = solver.Solve()
  
    if status == pywraplp.Solver.OPTIMAL:
        print('Solução ótima encontrada!')
        print(f'Total de trabalhadores: {int(solver.Objective().Value())}')
        for i in range(days):
            print(f'Trabalhadores que começam no dia {i+1}: {int(x[i].solution_value())}')
    else:
        print('Nenhuma solução ótima encontrada.')

wworkforce_scheduling()