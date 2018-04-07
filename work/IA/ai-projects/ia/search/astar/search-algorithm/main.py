import astar
import os
import sys
import csv
import math
from difflib import SequenceMatcher


class Cruzamento:

    def __init__(self, id, name, position):
        self.id = id
        self.name = name
        self.position = position
        self.links = []

    def __repr__(self):
        print("Ponto [{}]".format(str(self.name)))

def build_data():
    """Cria o mapa a partir do arquivo de cruzamentos"""
    cruzamentos = {}
    rootdir = os.path.dirname(os.path.abspath(sys.argv[0]))
    r = csv.reader(open(os.path.join(rootdir, 'cruzamentos.csv')))
    next(r)  # pula a primeira linha (cabeçalho)
    for record in r:
        id = int(record[0])
        latitude = float(record[1])
        longitude = float(record[2])
        name = record[3]
        cruzamentos[id] = Cruzamento(id, name, (latitude, longitude))

    r = csv.reader(open(os.path.join(rootdir, 'rotas.csv')))
    next(r)  # pula a primeira linha (cabeçalho)
    for id1, id2, savg in r:
        id1 = int(id1)
        id2 = int(id2)
        speed_average = float(savg)
        cruzamentos[id1].links.append((cruzamentos[id2], speed_average))
    return cruzamentos


def get_cruzamento_by_name(cruzamentos, name):
    """pega o cruzamento pelo nome do ponto"""
    name = name.lower()
    ratios = [(SequenceMatcher(None, name, v.name.lower()).ratio(), v) for v in cruzamentos.values()]

    best = max(ratios, key=lambda a: a[0])
    if best[0] > 0.7:
        return best[1]
    else:
        return None


def get_path(s1, s2 , use_speed_average=False):
    """ executa a busca A* """



    def distance(n1, n2):

        """calcula a distancia entre dois cruzamentos"""
        latA, longA = n1.position
        latB, longB = n2.position

        # convert degres to radians!!
        latA, latB, longA, longB = map(
            lambda d: d * math.pi / 180, (latA, latB, longA, longB))

        x = (longB - longA) * math.cos((latA + latB) / 2)
        y = latB - latA

        return math.hypot(x, y)

    return astar.find_path(s1, s2, neighbors_fnct=lambda s: s.links, heuristic_cost_estimate_fnct=distance, distance_between_fnct=distance, use_speed_average=use_speed_average)


if __name__ == '__main__':

    cruzamentos = build_data()

    station1 = get_cruzamento_by_name(cruzamentos, "A")
    print('Ir de : ' + station1.name)
    station2 = get_cruzamento_by_name(cruzamentos, "M")
    print('Para : ' + station2.name)
    print('-' * 80)


    path = get_path(station1, station2, True)

    if path:
        for s in path:
            print(s.name)
    else:
        raise Exception('caminho não encontrado!')
