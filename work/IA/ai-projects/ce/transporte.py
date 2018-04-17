import math


# mersenne twister
# aimotion.blogspot

def ifzero(n):
    return 1 if n == 0 else n


class Client:

    def __init__(self):
        self.rotas = []

    def imprime_informacoes_da_rota(self):

        quantidade_necessaria_caminhoes = 0

        for rota in self.rotas:
            quantidade_necessaria_caminhoes += rota.max_caminhoes_para_atender_a_rota()
            print("------------------------------------------------------------------------------------")
            print("Montadora : {} | Origem : {} | Destino : {} | Número máximo de caminhões nessa rota : {} | Tempo de viagem {} horas, Lucro por viagem : {}"
                  .format(rota.montadora, rota.origem, rota.destino, rota.max_caminhoes_para_atender_a_rota(), rota.tempo_de_viagem(), rota.lucro_por_viagem()))

        print(quantidade_necessaria_caminhoes)

    def __repr__(self):
        print(list(self.rotas))


class Route:

    CARGA_MAXIMA_DE_VEICULOS = 11
    TOTAL_HORAS_DIA = 24
    TOTAL_DIAS_MES = 30
    TOTAL_HORAS_MES = TOTAL_HORAS_DIA * TOTAL_DIAS_MES
    TEMPO_CARREGAMENTO = 1
    TEMPO_DESCARREGAMENTO = 2
    VELOCIDADE_MEDIA_CARREGADO = 50
    VELOCIDADE_MEDIA_DESCARREGADO = 72

    def __init__(self, montadora, origem, destino, demanda_veiculos, distancia, custo_por_viagem, remuneracao_por_viagem):
        self.montadora = montadora
        self.origem = origem
        self.destino = destino
        self.demanda_veiculos = demanda_veiculos
        self.distancia = distancia
        self.custo_por_viagem = custo_por_viagem
        self.remuneracao_por_viagem = remuneracao_por_viagem

    def tempo_de_viagem(self):
        """calcula o tempo necessario para ida e volta de uma rota"""

        tempo_ida = math.ceil(self.distancia / Route.VELOCIDADE_MEDIA_CARREGADO)
        tempo_volta = math.ceil(self.distancia / Route.VELOCIDADE_MEDIA_DESCARREGADO)
        return math.ceil(tempo_ida + tempo_volta + Route.TEMPO_CARREGAMENTO + Route.TEMPO_DESCARREGAMENTO)

    def demanda_viagens(self):
        """calcula a demanda de viagens para uma rota, arrendonda para baixo. Um caminhão sempre carrega 11 veiculos"""

        return math.floor(self.demanda_veiculos / Route.CARGA_MAXIMA_DE_VEICULOS)

    def max_viagens_caminhao(self):
        """calcula o número máximo de viagens que um caminhão pode fazer para atender uma rota no mẽs"""

        tempo_de_viagem = self.tempo_de_viagem()
        tempo_total_de_viagens_mes = 0
        total_de_viagens = 0
        while True:
            tempo_total_de_viagens_mes += tempo_de_viagem
            if tempo_total_de_viagens_mes > Route.TOTAL_HORAS_MES:
                break
            total_de_viagens += 1

        return total_de_viagens

    def max_veiculos_transportados_mes(self):
        return self.max_viagens_caminhao() * Route.CARGA_MAXIMA_DE_VEICULOS

    def max_caminhoes_para_atender_a_rota(self):
        """calcula o número máximo de caminhões necessários para atender uma rota em um mês"""

        max_viagens_caminhao = self.max_viagens_caminhao()
        demanda_viagens_mes = self.demanda_viagens()
        total_viagens_atendidas = 0
        nr_caminhoes_rota = 0

        while True:
            total_viagens_atendidas += max_viagens_caminhao
            nr_caminhoes_rota += 1
            if total_viagens_atendidas > demanda_viagens_mes:
                break
        return ifzero(nr_caminhoes_rota)

    def lucro_por_viagem(self):
        """retorna o lucro de uma rota"""

        return self.remuneracao_por_viagem - self.custo_por_viagem


gms_scs_rio = Route(montadora="GMS", origem="SCS", destino="RIO", demanda_veiculos=1701, distancia=448, custo_por_viagem=7667, remuneracao_por_viagem=10703)
gms_scs_bsb = Route(montadora="GMS", origem="SCS", destino="BSB", demanda_veiculos=1039, distancia=1021, custo_por_viagem=22509, remuneracao_por_viagem=24398)
gms_scs_cnf = Route(montadora="GMS", origem="SCS", destino="CNF", demanda_veiculos=1072, distancia=589, custo_por_viagem=9902, remuneracao_por_viagem=14069)
gms_scs_cwb = Route(montadora="GMS", origem="SCS", destino="CWB", demanda_veiculos=975, distancia=445, custo_por_viagem=7010, remuneracao_por_viagem=10626)
gms_scs_rec = Route(montadora="GMS", origem="SCS", destino="REC", demanda_veiculos=374, distancia=2709, custo_por_viagem=64803, remuneracao_por_viagem=64746)

cliente = Client()
cliente.rotas.append(gms_scs_rio)
cliente.rotas.append(gms_scs_bsb)
cliente.rotas.append(gms_scs_cnf)
cliente.rotas.append(gms_scs_cwb)
cliente.rotas.append(gms_scs_rec)

rnt_sjp_sp = Route(montadora="RNT", origem="SJP", destino="SAO", demanda_veiculos=1903, distancia=413, custo_por_viagem=5629, remuneracao_por_viagem=10615)
rnt_sjp_rio = Route(montadora="RNT", origem="SJP", destino="RIO", demanda_veiculos=684, distancia=853, custo_por_viagem=14539, remuneracao_por_viagem=21923)
rnt_sjp_cnf = Route(montadora="RNT", origem="SJP", destino="CNF", demanda_veiculos=431, distancia=1001, custo_por_viagem=16760, remuneracao_por_viagem=25729)
rnt_sjp_poa = Route(montadora="RNT", origem="SJP", destino="POA", demanda_veiculos=218, distancia=728, custo_por_viagem=12407, remuneracao_por_viagem=18711)

# rnt = Client("RNT")
cliente.rotas.append(rnt_sjp_sp)
cliente.rotas.append(rnt_sjp_rio)
cliente.rotas.append(rnt_sjp_cnf)
cliente.rotas.append(rnt_sjp_poa)

frd_sbc_rio = Route(montadora="FRD", origem="SBC", destino="RIO", demanda_veiculos=953, distancia=465, custo_por_viagem=7739, remuneracao_por_viagem=12606)
frd_sbc_cwb = Route(montadora="FRD", origem="SBC", destino="CWB", demanda_veiculos=547, distancia=434, custo_por_viagem=6645, remuneracao_por_viagem=11759)
frd_sbc_poa = Route(montadora="FRD", origem="SBC", destino="POA", demanda_veiculos=304, distancia=1162, custo_por_viagem=19279, remuneracao_por_viagem=31504)

# frd = Client("FRD")
cliente.rotas.append(frd_sbc_rio)
cliente.rotas.append(frd_sbc_cwb)
cliente.rotas.append(frd_sbc_poa)

fat_bet_sao = Route(montadora="FAT", origem="BET", destino="SAO", demanda_veiculos=5246, distancia=554, custo_por_viagem=7570, remuneracao_por_viagem=12188)
fat_bet_bsb = Route(montadora="FAT", origem="BET", destino="BSB", demanda_veiculos=1152, distancia=746, custo_por_viagem=16344, remuneracao_por_viagem=16412)
fat_bet_cwb = Route(montadora="FAT", origem="BET", destino="CWB", demanda_veiculos=1081, distancia=962, custo_por_viagem=15068, remuneracao_por_viagem=21164)
fat_bet_rec = Route(montadora="FAT", origem="BET", destino="REC", demanda_veiculos=414, distancia=2153, custo_por_viagem=51191, remuneracao_por_viagem=47366)

# fat = Client("FAT")
cliente.rotas.append(fat_bet_sao)
cliente.rotas.append(fat_bet_bsb)
cliente.rotas.append(fat_bet_cwb)
cliente.rotas.append(fat_bet_rec)


vkw_dia_rio = Route(montadora="VKW", origem="DIA", destino="RIO", demanda_veiculos=1689, distancia=465, custo_por_viagem=10619, remuneracao_por_viagem=11528)
vkw_dia_bsb = Route(montadora="VKW", origem="DIA", destino="BSB", demanda_veiculos=1031, distancia=1027, custo_por_viagem=30125, remuneracao_por_viagem=25465)
vkw_dia_cwb = Route(montadora="VKW", origem="DIA", destino="CWB", demanda_veiculos=968, distancia=434, custo_por_viagem=9118, remuneracao_por_viagem=10758)
vkw_dia_poa = Route(montadora="VKW", origem="DIA", destino="POA", demanda_veiculos=538, distancia=1162, custo_por_viagem=26452, remuneracao_por_viagem=28820)

# vkw = Client("VKW")
cliente.rotas.append(vkw_dia_rio)
cliente.rotas.append(vkw_dia_bsb)
cliente.rotas.append(vkw_dia_cwb)
cliente.rotas.append(vkw_dia_poa)

hyd_pir_sao = Route(montadora="HYD", origem="PIR", destino="SAO", demanda_veiculos=1360, distancia=157, custo_por_viagem=1609, remuneracao_por_viagem=4961)
hyd_pir_cnf = Route(montadora="HYD", origem="PIR", destino="CNF", demanda_veiculos=308, distancia=650, custo_por_viagem=8431, remuneracao_por_viagem=20537)
hyd_pir_cwb = Route(montadora="HYD", origem="PIR", destino="CWB", demanda_veiculos=281, distancia=539, custo_por_viagem=6549, remuneracao_por_viagem=17028)
hyd_pir_rec = Route(montadora="HYD", origem="PIR", destino="REC", demanda_veiculos=108, distancia=2745, custo_por_viagem=50587, remuneracao_por_viagem=86746)
hyd_pir_poa = Route(montadora="HYD", origem="PIR", destino="POA", demanda_veiculos=156, distancia=1267, custo_por_viagem=16701, remuneracao_por_viagem=40040)

# hyd = Client("HYD")
cliente.rotas.append(hyd_pir_sao)
cliente.rotas.append(hyd_pir_cnf)
cliente.rotas.append(hyd_pir_cwb)
cliente.rotas.append(hyd_pir_rec)
cliente.rotas.append(hyd_pir_poa)


pgt_prl_sao = Route(montadora="PGT", origem="PRL", destino="SAO", demanda_veiculos=458, distancia=287, custo_por_viagem=2249, remuneracao_por_viagem=9427)
pgt_prl_cnf = Route(montadora="PGT", origem="PRL", destino="CNF", demanda_veiculos=104, distancia=421, custo_por_viagem=4076, remuneracao_por_viagem=13838)
pgt_prl_cwb = Route(montadora="PGT", origem="PRL", destino="CWB", demanda_veiculos=95, distancia=698, custo_por_viagem=6292, remuneracao_por_viagem=22946)

# pgt = Client("PGT")
cliente.rotas.append(pgt_prl_sao)
cliente.rotas.append(pgt_prl_cnf)
cliente.rotas.append(pgt_prl_cwb)


import random
import inspyred
import time
import pylab


def generate_candidates(random, args):
    cromossome = []
    for trip in cliente.rotas:
        max_truck = random.randint(0, trip.max_caminhoes_para_atender_a_rota())
        cromossome.append(max_truck)
    return cromossome


def fitness(cromossome):
    lucro_total = 0
    nr_caminhoes = 0
    for i in range(0, len(cromossome)):
        gene = cromossome[i]
        if gene > 0:
            nr_caminhoes += gene
            # print("gene {}".format(gene))

            max_viagens = gene * cliente.rotas[i].max_viagens_caminhao()
            demanda = cliente.rotas[i].demanda_viagens()
            lucro_por_viagem = cliente.rotas[i].lucro_por_viagem()
            # print("Max viagens caminhao {}".format(cliente.rotas[i].max_viagens_caminhao()))
            # print("Max viagens {}".format(max_viagens))
            # print("Demanda maxima da rota {}".format(demanda))

            # se tiver caminhão ocioso calcula a demanda total
            if max_viagens > demanda:
                lucro_rota = demanda * lucro_por_viagem

            # se não tiver caminhão ocioso calcula o lucro sobre o total de viagens
            else:
                lucro_rota = max_viagens * lucro_por_viagem
            lucro_total += lucro_rota

    return lucro_total - penalizacao(lucro_total, nr_caminhoes)


def penalizacao(lucro_total, nr_caminhoes):
    lucro_medio_caminhao = lucro_total / nr_caminhoes
    penalizacao = max(0, 1.7 * lucro_medio_caminhao * (nr_caminhoes - 70))
    return penalizacao

def count_vehicle(cromossome):
    nr_trucks = 0
    cnt_route = 0
    for i in range(0, len(cromossome)):
        gene = cromossome[i]
        nr_trucks += gene
        if gene > 0:
            cnt_route += 1
    return nr_trucks, cnt_route, cnt_route/28


@inspyred.ec.evaluators.evaluator
def evaluate_trip_candidates(candidate, args):
    return fitness(candidate)


def setup_ga():

    #seed = int(time.time())
    seed = 1523840859
    rand = random.Random()
    rand.seed(seed)

    # Evolutionary computation representing a canonical genetic algorithm.
    ga = inspyred.ec.GA(rand)
    ga.observer = [inspyred.ec.observers.stats_observer]  # inspyred.ec.observers.plot_observer inspyred.ec.observers.best_observer

    # condição de término pelo máximo de avaliações
    ga.terminator = inspyred.ec.terminators.evaluation_termination

    # mutação binária
    # ga.variator = inspyred.ec.variators.bit_flip_mutation

    return ga, seed


def ga_transporte(ga):

    # ga.analysis =  inspyred.ec.analysis.generation_plot("teste.png")

    final_pop = ga.evolve(evaluator=evaluate_trip_candidates,
                          generator=generate_candidates,
                          max_evaluations=3400,
                          mutation_rate=0.8,
                          pop_size=200,
                          crossover_rate=0.9,
                          num_selected=80,
                          num_crossover_points=1
                          )

    final_pop.sort(reverse=True)
    print("Terminated due to {0}.".format(ga.termination_cause))
    print(final_pop[0])


    pylab.show()

    print("lucro total {}".format(fitness(final_pop[0].candidate)))
    print("Count Veiculos {}".format(count_vehicle(final_pop[0].candidate)))
    print("seed = {} ".format(seed))
    return final_pop[0].fitness



def frequencyDistribution(data):
    return {i: data.count(i) for i in data}


if __name__ == "__main__":
    # cliente.imprime_informacoes_da_rota()

    total_values = []

    from datetime import datetime

    start_time = datetime.now()
    ga, seed = setup_ga()
    total_values.append(ga_transporte(ga))

    print(frequencyDistribution(total_values))
    time_elapsed = datetime.now() - start_time

    print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))


