from __future__ import division
import json

# configuracoes
scheduler_range = 20

# ler tarefas do json
with open('tarefas.json', 'r') as f:
    tarefas = json.load(f)

# calcular a carga no processador
load = 0.0
for t in tarefas:
    load += t[1] / t[2]

# printar cabecalho
print "Conjunto de tarefas:\n"
for t in tarefas:
    print "%s:\t(%d, %d)" % (t[0], t[1], t[2])

print "\nUso do processador: %.2f %%" % (load * 100)
if load > 1:
    print "\nConjunto nao escalonavel"
    exit()

print "\nEscalonamento:\n"

# preparar o conjunto de tarefas
tarefas.sort(key=lambda x: x[2])

for t in tarefas:
    t.append(t[1])
    t.append(0)

scheduler = ""
mark = ""
time = ""
last = ""

for x in xrange(scheduler_range):
    # atualizando os marcadores de acordo com o tamanho da escala
    mark += "|  "
    time += "%2d " % (x)

    # para ter controle de ociosidade
    ctrl = 0

    # atualizar os deadlines
    temp = []
    for t in tarefas:
        if x % t[2] == 0:
            temp.append(t)
    for t in temp:
        tarefas.remove(t)
        t[4] += t[2]
        t[3] = t[1]
        tarefas.append(t)

    # ordenar a prioridade
    tarefas.sort(key=lambda x: x[4])

    # verificar por ordem de prioridade se alguma tarefa tem carga a executar
    for t in tarefas:
        if t[3] > 0:
            if last == t[0]:
                scheduler += "   "
            else:
                scheduler += "|" + t[0]
            last = t[0]
            ctrl = 1
            t[3] -= 1
            break            

    # imprimir ociosidade
    if ctrl == 0:
        if last == "* ":
            scheduler += "   "
        else:
            scheduler += "|* "
        last = "* "


print scheduler
print mark
print time

print "\n* Processador ocioso"
