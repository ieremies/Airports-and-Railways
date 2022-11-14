from sys import argv
import gurobipy as gp
from gurobipy import GRB
from math import ceil

# ================= Leitura da instância ==============
airport = {}
railway = {}
with open(argv[1], "r") as fd:
    k = int(fd.readline())
    for l in fd:
        l = l.split()
        if len(l) == 2:
            airport[int(l[0])] = int(l[1])
        elif len(l) == 3:
            railway[(int(l[0]), int(l[1]))] = float(l[2])

nodes = list(airport)
nnodes = len(nodes)
# Adicionando o s
airport["s"] = 0
for n in airport:
    railway[(n, "s")] = float("inf")
    railway[("s", n)] = 0

# ================== Modelo ============================

m = gp.Model()
m.modelSense = GRB.MINIMIZE

y = {a: m.addVar(obj=airport[a], vtype=GRB.BINARY, name=f"y_{a}") for a in airport}
z = {r: m.addVar(obj=railway[r], vtype=GRB.BINARY, name=f"z_{r}") for r in railway}
# Rodando alguns experimentos, parece que podemos relaxar x a ser contínuo
x = {
    r: m.addVar(lb=0, ub=k, obj=0, vtype=GRB.CONTINUOUS, name=f"x_{r}") for r in railway
}

m.update()

# Restrição de fluxo
for i in nodes:
    c = gp.LinExpr()
    for j in nodes:
        c += x[(i, j)] - x[(j, i)]
    c += x[("s", i)]
    m.addConstr(c == 1)

# Restrição de abertura de aeroporto
m.addConstrs(x[("s", n)] <= k * y[n] for n in airport)

# Restrição de abertura de railway
m.addConstrs(x[r] <= k * z[r] for r in railway)

# Corte para quantidade de aeroportos abertos
c = gp.LinExpr()
for i in range(nnodes):
    c += y[i]
m.addConstr(c >= ceil(nnodes / k))

# for i in nodes:
#     c = gp.LinExpr()
#     for j in nodes:
#         c += x[(i, j)]
#     m.addConstr(c == 1)

m.optimize()
