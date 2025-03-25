from ortools.linear_solver import pywraplp

def dietProblem():
    solver = pywraplp.Solver.CreateSolver('SCIP')

    if not solver:
        print('Solver não pode ser criado.')
        return

    x = []
    for i in range(6):
        x.append(solver.IntVar(0.0, solver.infinity(), f'x{i+1}'))

    print("Número de variáveis =", solver.NumVariables())

    # Função objetivo: 3x1 + 24x2 + 13x3 + 9x4 + 20x5 + 19x6
    objective = solver.Objective()
    coefficients = [3, 24, 13, 9, 20, 19]
    for i in range(6):
        objective.SetCoefficient(x[i], coefficients[i])
    objective.SetMinimization()

    # Restrições
    # 110x1 + 265x2 + 160x3 + 160x4 + 420x5 + 260x6 >= 2000
    constraint1 = solver.Constraint(2000, solver.infinity())
    constraint1.SetCoefficient(x[0], 110)
    constraint1.SetCoefficient(x[1], 265)
    constraint1.SetCoefficient(x[2], 160)
    constraint1.SetCoefficient(x[3], 160)
    constraint1.SetCoefficient(x[4], 420)
    constraint1.SetCoefficient(x[5], 260)

    # 4x1 + 32x2 + 13x3 + 8x4 + 4x5 + 14x6 >= 55
    constraint2 = solver.Constraint(55, solver.infinity())
    constraint2.SetCoefficient(x[0], 4)
    constraint2.SetCoefficient(x[1], 32)
    constraint2.SetCoefficient(x[2], 13)
    constraint2.SetCoefficient(x[3], 8)
    constraint2.SetCoefficient(x[4], 4)
    constraint2.SetCoefficient(x[5], 14)

    # 2x1 + 12x2 + 54x3 + 285x4 + 22x5 + 80x6 >= 800
    constraint3 = solver.Constraint(800, solver.infinity())
    constraint3.SetCoefficient(x[0], 2)
    constraint3.SetCoefficient(x[1], 12)
    constraint3.SetCoefficient(x[2], 54)
    constraint3.SetCoefficient(x[3], 285)
    constraint3.SetCoefficient(x[4], 22)
    constraint3.SetCoefficient(x[5], 80)
   
    solver.Constraint(0, 4).SetCoefficient(x[0], 1)  # x1 <= 4
    solver.Constraint(0, 3).SetCoefficient(x[1], 1)  # x2 <= 3
    solver.Constraint(0, 2).SetCoefficient(x[2], 1)  # x3 <= 2
    solver.Constraint(0, 8).SetCoefficient(x[3], 1)  # x4 <= 8
    solver.Constraint(0, 2).SetCoefficient(x[4], 1)  # x5 <= 2
    solver.Constraint(0, 2).SetCoefficient(x[5], 1)  # x6 <= 2

    status = solver.Solve()

    # Solução
    if status == pywraplp.Solver.OPTIMAL:
        print('Solução ótima encontrada.')
        print(f'Custo total: {objective.Value()}')
        for i in range(6):
            print(f'x{i+1} = {x[i].solution_value()}')
    else:
        print('Não foi possível encontrar uma solução ótima.')

dietProblem()