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

#Variáveis inteiras não-negativas para penalidades
a_p = {p: solver.IntVar(0, solver.infinity(), f'a_p[{p}]') for p in P} #Penalidade a um professor quando é associado a uma turma fora do subconjunto Tp das turmas que compõem o perfil acadêmico do mesmo
b_p = {p: solver.IntVar(0, solver.infinity(), f'b_p[{p}]') for p in P} #Penalidade a um professor quando é associado a um dia fora do seu subconjunto Dp de dias preferíveis para lecionar

#Coeficientes inteiros positivos para a FO
alpha = solver.IntVar(0, solver.infinity(), 'alpha') #Atribuição de um professor a uma turma fora de seu perfil
beta = solver.IntVar(0, solver.infinity(), 'beta') #Associação entre um professor p ∈ P e um dia fora de Dp