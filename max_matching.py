from ortools.linear_solver import pywraplp

def max_matching(vertices, edges):
    solver = pywraplp.Solver.CreateSolver('SCIP')

    if not solver:
        print('Solver não pode ser criado.')
        return
    
    #Variáveis binárias xe indicando se uma aresta e está no emparelhamento máximo
    x = {e: solver.BoolVar(f'x_{e}') for e in edges}
    
    #Restrição: Cada vértice pode estar em no máximo uma aresta do emparelhamento
    for v in vertices:
        solver.Add(sum(x[e] for e in edges if v in e) <= 1)
    
    #Função objetivo: Maximizar o número de arestas no emparelhamento
    solver.Maximize(solver.Sum(x[e] for e in edges))
    
    print("Dados do problema:")
    print("Número de variáveis =", solver.NumVariables())

    #Solução
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print('Solução ótima encontrada.')
        matching = [e for e in edges if x[e].solution_value() > 0.5]
        return matching
    else:
        print('Não foi possível encontrar uma solução ótima.')
        return None

#APP
vertices = {1, 2, 3, 4, 5, 6}
edges = {(1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 6)}

matching = max_matching(vertices, edges)
print("Emparelhamento máximo:", matching)
