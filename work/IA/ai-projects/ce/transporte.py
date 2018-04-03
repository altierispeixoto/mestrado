import math


def ifzero(n):
    return 1 if n == 0 else n

class Client:

    def __init__(self):
        self.trips = []

    def __repr__(self):
        print(self.name, list(self.trips))


class Trip:

    MAX_VEHICLE_TRIP = 11
    TOTAL_HOURS_MONTH = 24 * 30
    NUMBER_HOURS_LOAD = 1
    NUMBER_HOURS_UNLOAD = 2
    SPEED_AVERAGE_LOADED = 50
    SPEED_AVERAGE_UNLOADED = 72

    def __init__(self, montadora, origem, destino,qtd_veiculos,distancia, custo_por_viagem,remuneracao_por_viagem):
        self.montadora = montadora
        self.origem = origem
        self.destino = destino
        self.qtd_veiculos = qtd_veiculos
        self.distancia = distancia
        self.custo_por_viagem = custo_por_viagem
        self.remuneracao_por_viagem = remuneracao_por_viagem

    def time_trip(self):
        return math.ceil((self.distancia/Trip.SPEED_AVERAGE_LOADED) + (self.distancia/Trip.SPEED_AVERAGE_UNLOADED) + Trip.NUMBER_HOURS_LOAD + Trip.NUMBER_HOURS_UNLOAD)

    def max_trip_demand(self):
        return math.floor(self.qtd_veiculos/Trip.MAX_VEHICLE_TRIP)

    def max_trips_truck(self):
        time_trip = self.time_trip()
        total_time_trip_month = 0
        total_trip_count = 0
        while True:
            total_time_trip_month += time_trip
            if total_time_trip_month > Trip.TOTAL_HOURS_MONTH:
                break
            total_trip_count += 1
        return total_trip_count

    def max_vehicle_transported_month(self):
        return self.max_trips_truck() * Trip.MAX_VEHICLE_TRIP

    def max_truck_number_demand_month(self):
        max_trip_truck = self.max_trips_truck()
        max_trip_demand_month = self.max_trip_demand()
        total_trip_attended = 0
        max_truck_demand = 0

        while True:
            total_trip_attended += max_trip_truck
            if total_trip_attended > max_trip_demand_month:
                break
            max_truck_demand += 1
        return ifzero(max_truck_demand)

    def lucro_por_viagem(self):
        return self.remuneracao_por_viagem - self.custo_por_viagem

    def __repr__(self):
        print("Montadora = {}".format(self.montadora))
        print("origem = {}".format(self.origem))
        print("destino = {}".format(self.destino))
        print("demanda de veiculos = {}".format(self.qtd_veiculos))
        print("distancia = {}".format(self.distancia))
        print("demanda de viagens = {}".format(self.max_trip_demand()))
        print("tempo de viagem [ida + volta ]= {}".format(self.time_trip()))
        print("Nº maximo de viagens nessa rota no mês = {}".format(self.max_trips_truck()))
        print("Nº maximo de veículos transportados no mês = {}".format(self.max_vehicle_transported_month()))
        print("nº maximo de caminhões para esta rota = {}".format(self.max_truck_number_demand_month()))

        print("Custo por viagem = {}".format(self.custo_por_viagem))
        print("Remuneracao por viagem = {}".format(self.remuneracao_por_viagem))
        print("Lucro por viagem = {}".format(self.lucro_por_viagem()))
        return "---------------------"


gms_scs_rio = Trip(montadora="GMS", origem="SCS", destino="RIO", qtd_veiculos=1701, distancia=448, custo_por_viagem=7667, remuneracao_por_viagem=10703)
gms_scs_bsb = Trip(montadora="GMS", origem="SCS", destino="BSB", qtd_veiculos=1039, distancia=1021, custo_por_viagem=22509, remuneracao_por_viagem=24398)
gms_scs_cnf = Trip(montadora="GMS", origem="SCS", destino="CNF", qtd_veiculos=1072, distancia=589, custo_por_viagem=9902, remuneracao_por_viagem=14069)
gms_scs_cwb = Trip(montadora="GMS", origem="SCS", destino="CWB", qtd_veiculos=975, distancia=445, custo_por_viagem=7010, remuneracao_por_viagem=10626)
gms_scs_rec = Trip(montadora="GMS", origem="SCS", destino="REC", qtd_veiculos=374, distancia=2709, custo_por_viagem=64803, remuneracao_por_viagem=64746)

cliente = Client()
cliente.trips.append(gms_scs_rio)
cliente.trips.append(gms_scs_bsb)
cliente.trips.append(gms_scs_cnf)
cliente.trips.append(gms_scs_cwb)
cliente.trips.append(gms_scs_rec)

rnt_sjp_sp = Trip(montadora="RNT", origem="SJP", destino="SAO", qtd_veiculos=1903, distancia=413, custo_por_viagem=5629, remuneracao_por_viagem=10615)
rnt_sjp_rio = Trip(montadora="RNT", origem="SJP", destino="RIO", qtd_veiculos=684, distancia=853, custo_por_viagem=14539, remuneracao_por_viagem=21923)
rnt_sjp_cnf = Trip(montadora="RNT", origem="SJP", destino="CNF", qtd_veiculos=431, distancia=1001, custo_por_viagem=16760, remuneracao_por_viagem=25729)
rnt_sjp_poa = Trip(montadora="RNT", origem="SJP", destino="POA", qtd_veiculos=218, distancia=728, custo_por_viagem=12407, remuneracao_por_viagem=18711)

# rnt = Client("RNT")
cliente.trips.append(rnt_sjp_sp)
cliente.trips.append(rnt_sjp_rio)
cliente.trips.append(rnt_sjp_cnf)
cliente.trips.append(rnt_sjp_poa)

frd_sbc_rio = Trip(montadora="FRD", origem="SBC", destino="RIO", qtd_veiculos=953, distancia=465, custo_por_viagem=7739, remuneracao_por_viagem=12606)
frd_sbc_cwb = Trip(montadora="FRD", origem="SBC", destino="CWB", qtd_veiculos=547, distancia=434, custo_por_viagem=6645, remuneracao_por_viagem=11759)
frd_sbc_poa = Trip(montadora="FRD", origem="SBC", destino="POA", qtd_veiculos=304, distancia=1162, custo_por_viagem=19279, remuneracao_por_viagem=31504)

# frd = Client("FRD")
cliente.trips.append(frd_sbc_rio)
cliente.trips.append(frd_sbc_cwb)
cliente.trips.append(frd_sbc_poa)

fat_bet_sao = Trip(montadora="FAT", origem="BET", destino="SAO", qtd_veiculos=5246, distancia=554, custo_por_viagem=7570, remuneracao_por_viagem=12188)
fat_bet_bsb = Trip(montadora="FAT", origem="BET", destino="BSB", qtd_veiculos=1152, distancia=746, custo_por_viagem=16344, remuneracao_por_viagem=16412)
fat_bet_cwb = Trip(montadora="FAT", origem="BET", destino="CWB", qtd_veiculos=1081, distancia=962, custo_por_viagem=15068, remuneracao_por_viagem=21164)
fat_bet_rec = Trip(montadora="FAT", origem="BET", destino="REC", qtd_veiculos=414, distancia=2153, custo_por_viagem=51191, remuneracao_por_viagem=47366)

# fat = Client("FAT")
cliente.trips.append(fat_bet_sao)
cliente.trips.append(fat_bet_bsb)
cliente.trips.append(fat_bet_cwb)
cliente.trips.append(fat_bet_rec)


vkw_dia_rio = Trip(montadora="VKW", origem="DIA", destino="RIO", qtd_veiculos=1689, distancia=465, custo_por_viagem=10619, remuneracao_por_viagem=11528)
vkw_dia_bsb = Trip(montadora="VKW", origem="DIA", destino="BSB", qtd_veiculos=1031, distancia=1027, custo_por_viagem=30125, remuneracao_por_viagem=25465)
vkw_dia_cwb = Trip(montadora="VKW", origem="DIA", destino="CWB", qtd_veiculos=968, distancia=434, custo_por_viagem=9118, remuneracao_por_viagem=10758)
vkw_dia_poa = Trip(montadora="VKW", origem="DIA", destino="POA", qtd_veiculos=538, distancia=1162, custo_por_viagem=26452, remuneracao_por_viagem=28820)

# vkw = Client("VKW")
cliente.trips.append(vkw_dia_rio)
cliente.trips.append(vkw_dia_bsb)
cliente.trips.append(vkw_dia_cwb)
cliente.trips.append(vkw_dia_poa)

hyd_pir_sao = Trip(montadora="HYD", origem="PIR", destino="SAO", qtd_veiculos=1360, distancia=157, custo_por_viagem=1609, remuneracao_por_viagem=4961)
hyd_pir_cnf = Trip(montadora="HYD", origem="PIR", destino="CNF", qtd_veiculos=308, distancia=650, custo_por_viagem=8431, remuneracao_por_viagem=20537)
hyd_pir_cwb = Trip(montadora="HYD", origem="PIR", destino="CWB", qtd_veiculos=281, distancia=539, custo_por_viagem=6549, remuneracao_por_viagem=17028)
hyd_pir_rec = Trip(montadora="HYD", origem="PIR", destino="REC", qtd_veiculos=108, distancia=2745, custo_por_viagem=50587, remuneracao_por_viagem=86746)
hyd_pir_poa = Trip(montadora="HYD", origem="PIR", destino="POA", qtd_veiculos=156, distancia=1267, custo_por_viagem=16701, remuneracao_por_viagem=40040)

# hyd = Client("HYD")
cliente.trips.append(hyd_pir_sao)
cliente.trips.append(hyd_pir_cnf)
cliente.trips.append(hyd_pir_cwb)
cliente.trips.append(hyd_pir_rec)
cliente.trips.append(hyd_pir_poa)


pgt_prl_sao = Trip(montadora="PGT", origem="PRL", destino="SAO", qtd_veiculos=458, distancia=287, custo_por_viagem=2249, remuneracao_por_viagem=9427)
pgt_prl_cnf = Trip(montadora="PGT", origem="PRL", destino="CNF", qtd_veiculos=104, distancia=421, custo_por_viagem=4076, remuneracao_por_viagem=13838)
pgt_prl_cwb = Trip(montadora="PGT", origem="PRL", destino="CWB", qtd_veiculos=95, distancia=698, custo_por_viagem=6292, remuneracao_por_viagem=22946)

# pgt = Client("PGT")
cliente.trips.append(pgt_prl_sao)
cliente.trips.append(pgt_prl_cnf)
cliente.trips.append(pgt_prl_cwb)


import random
import inspyred
import time
import pylab

def generate_candidates(random, args):
    cromossome = []
    for trip in cliente.trips:
        max_truck = random.randint(0, trip.max_truck_number_demand_month())
        cromossome.append(max_truck)
    #print(c.name, trip.origem, trip.destino, max_truck)
    return cromossome

#print(list(cromossome))


def fitness(cromossome):
    nr_trucks = 0
    lucro_total = 0
    cnt_route = 0
    for i in range(0, len(cromossome)):
        gene = cromossome[i]
        nr_trucks += gene
        lucro_viagem = cliente.trips[i].lucro_por_viagem() * cliente.trips[i].max_trips_truck() * gene
        lucro_total += lucro_viagem
        #print("gene {}".format(gene))
        #print(cliente.trips[i].montadora,cliente.trips[i].origem,cliente.trips[i].destino,gene,lucro_viagem )
        if gene > 0:
            cnt_route += 1
    #print(nr_trucks, lucro_total, cnt_route/28)
    return lucro_total


def count_vehicle(cromossome):
    nr_trucks = 0
    cnt_route = 0
    for i in range(0, len(cromossome)):
        gene = cromossome[i]
        nr_trucks += gene
        if gene > 0:
            cnt_route += 1
    #print(nr_trucks, lucro_total, cnt_route/28)
    return nr_trucks,cnt_route



@inspyred.ec.evaluators.evaluator
def evaluate_trip_candidates(candidate, args):
    lucro_total = fitness(candidate)

    # if total_weight > MAX_CAPACITY:
    #     return MAX_CAPACITY - total_weight
    # else:
    return lucro_total


rand = random.Random()
rand.seed(int(time.time()))


ga            = inspyred.ec.GA(rand)

ga.observer   = [inspyred.ec.observers.stats_observer] #inspyred.ec.observers.plot_observer inspyred.ec.observers.best_observer
ga.terminator = inspyred.ec.terminators.evaluation_termination
ga.variator   = inspyred.ec.variators.bit_flip_mutation
#ga.analysis =  inspyred.ec.analysis.generation_plot("teste.png")

final_pop = ga.evolve(evaluator=evaluate_trip_candidates,
                      generator=generate_candidates,
                      max_evaluations=70000,
                      maximize=True,
                      mutation_rate=1,
                      pop_size=15000,
                      crossover_rate=10,
                      num_selected=3500,
                      num_crossover_points=1
                      )


final_pop.sort(reverse=True)
for ind in final_pop:
    print(str(ind))

#pop.sort(reverse=True)
print("Terminated due to {0}.".format(ga.termination_cause))
print(final_pop[0])

print(count_vehicle(final_pop[0].candidate))
#total_weight, total_value = knapsack_calc(final_pop[0].candidate)
#print("Peso calculado = {} ,  valor calculado = {}".format(total_weight,total_value))

pylab.show()