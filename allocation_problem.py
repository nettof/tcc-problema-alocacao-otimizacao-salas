from typing import Set, Dict
from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

#Conjuntos
P: Set[int] = set()  #Professores
T: Set[int] = set()  #Turmas
D: Set[int] = set()  #Dias da semana
D_feriados: Set[int] = set()  #D' - Dias com feriados
H: Set[int] = set()  #Slots de horários
S: Set[int] = set()  #Salas

#Subconjuntos
T_p: Dict[int, Set[int]] = dict()  #T_p: turmas do professor p
D_p: Dict[int, Set[int]] = dict()  #D_p: dias preferíveis do professor p

#Parâmetros
ch_T_t: Dict[int, int] = dict()  #Carga horária teórica da turma t
ch_P_t: Dict[int, int] = dict()  #Carga horária prática da turma t
ch_p: Dict[int, int] = dict()    #Carga horária do professor

#Variáveis
z_pi = {(p, i): solver.BoolVar(f'z_pi[{p},{i}]') for p in P for i in D} #Associação entre um professor p e um dia da semana i
x_pt = {(p, t): solver.BoolVar(f'x_pt[{p},{t}]') for p in P for t in T} #Associação entre um professor p e uma turma t
y_P_tijk = {(t, i, j, k): solver.BoolVar(f'y_P_tijk[{t},{i},{j},{k}]') for t in T for i in D for j in H for k in S} #Associação de uma turma t ∈ T com carga horária prática a um i ∈ D, j ∈ H e k ∈ S
y_T_tijk = {(t, i, j, k): solver.BoolVar(f'y_T_tijk[{t},{i},{j},{k}]') for t in T for i in D for j in H for k in S} #Associação de uma turma t ∈ T com carga horária teórica a um i ∈ D, j ∈ H e k ∈ S
y_tijk = {(t, i, j, k): solver.IntVar(0, solver.infinity(), f'y_tijk[{t},{i},{j},{k}]') for t in T for i in D for j in H for k in S} #Carga horária total da turma sem distinguir carga horária teórica da prática
w_ptijk = {(p, t, i, j, k): solver.BoolVar(f'w_ptijk[{p},{t},{i},{j},{k}]') for p in P for t in T for i in D for j in H for k in S} #Produto linearizado de x_pt * y_tijk

#Variáveis inteiras não-negativas para penalidades
a_p = {p: solver.IntVar(0, solver.infinity(), f'a_p[{p}]') for p in P} #Penalidade a um professor quando é associado a uma turma fora do subconjunto Tp das turmas que compõem o perfil acadêmico do mesmo
b_p = {p: solver.IntVar(0, solver.infinity(), f'b_p[{p}]') for p in P} #Penalidade a um professor quando é associado a um dia fora do seu subconjunto Dp de dias preferíveis para lecionar

#Coeficientes inteiros positivos para a FO
alpha = solver.IntVar(0, solver.infinity(), 'alpha') #Atribuição de um professor a uma turma fora de seu perfil
beta = solver.IntVar(0, solver.infinity(), 'beta') #Associação entre um professor p ∈ P e um dia fora de Dp

alpha = 1
beta = 1

#FO
solver.Minimize(alpha * solver.Sum(a_p[p] for p in P) + beta * solver.Sum(b_p[p] for p in P))

#Restrição 5.27 - Assegura que toda turma tenha apenas um professor associado a mesma
for t in T:
    solver.Add(solver.Sum(x_pt[(p, t)] for p in P) == 1)

#Restrição 5.28 - Descreve quando um professor é vinculado a uma turma que não pertence ao grupo de turmas constantes em seu perfil
for p in P:
    solver.Add(solver.Sum(x_pt[(p, t)] for t in T if t not in T_p.get(p, set())) <= a_p[p])

#Restrição 5.29 - Garante que todo professor cumpra sua carga horária de trabalho
for p in P:
    solver.Add(solver.Sum((ch_T_t[t] + ch_P_t[t]) * x_pt[(p, t)] for t in T) == ch_p[p])

#Restrição 5.30 - Toda turma tem que cumprir sua carga horária teórica
for t in T:
    solver.Add(solver.Sum(y_T_tijk[(t, i, j, k)] for i in D for j in H for k in S) == ch_T_t[t] // 2)

#Restrição 5.31 - Toda turma tem que cumprir sua carga horária prática
for t in T:
    solver.Add(solver.Sum(y_P_tijk[(t, i, j, k)] for i in D for j in H for k in S) == ch_P_t[t] // 2)

#Restrição 5.32 - Certifica que para qualquer dia, slot de horário e sala será associado apenas a uma turma
for i in D:
    for j in H:
        for k in S:
            solver.Add(solver.Sum(y_tijk[(t, i, j, k)] for t in T <= 1))

#Restrição 5.33 - Representa a associação entre a y_T_tijk e y_P_tijk para que possa ser valorado y_tijk
for t in T:
    for i in D:
        for j in H:
            for k in S:
                solver.Add(
                    y_tijk[(t, i, j, k)] == y_T_tijk[(t, i, j, k)] + y_P_tijk[(t, i, j, k)]
                )

#Restrição 5.34 - Garante a vinculação de um professor a uma turma com mesmo dia, slot de horário e sala
for p in P:
    for t in T:
        for i in D:
            for j in H:
                for k in S:
                    solver.Add(
                        w_ptijk[(p, t, i, j, k)] <= z_pi[[(p, i)]]
                    )

#Restrições 5.46 - 5.48 linearização do produto x_pt * y_tijk
#Restrição 5.46
for p in P:
    for t in T:
        for i in D:
            for j in H:
                for k in S:
                    solver.Add(
                        w_ptijk[(p, t, i, j, k)] <= x_pt[(p, t)]
                    )

#Restrição 5.47
for p in P:
    for t in T:
        for i in D:
            for j in H:
                for k in S:
                    solver.Add(
                        w_ptijk[(p, t, i, j, k)] <= y_tijk[(t, i, j, k)]
                    )

#Restrição 5.48
for p in P:
    for t in T:
        for i in D:
            for j in H:
                for k in S:
                    solver.Add(
                        w_ptijk[(p, t, i, j, k)] >= x_pt[(p, t)] + y_tijk[(t, i, j, k)] - 1
                    )

#Restrição 5.35 - Descreve quando um professor é associado a um dia que não está compreendido dentro do seu conjunto de dias preferenciais para aulas
for p in P:
    solver.Add(
        solver.Sum(
            z_pi[(p, i)] for i in D if i not in D_p.get(p, set())
        ) <= b_p[p]
    )

#Restrição 5.36 - Assegura que uma turma teórica venha primeiro que uma turma prática
for t in T:
    for i in D:
        for i_linha in D_feriados:
            if i < i_linha:
                 for j in H:
                     for j_linha in H:
                         for k in S:
                             for k_linha in S:
                                 solver.Add(
                                     y_P_tijk[(t, i, j, k)] <= 1 - y_T_tijk[(t, i_linha, j_linha, k_linha)]
                                 )