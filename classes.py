import random
import json
import itertools

class Time:
    def __init__(self, jogadores, nome) -> None:
        self.nome = nome
        self.jogadores = jogadores
        self.titulares = jogadores[:11]
        self.reservas = jogadores[11:]
        self.pontos = 0
        self.forca = 0
        for j in self.titulares:
            self.forca += j.forca
        self.jogadores[0].goleiro = True
        self.jogadores[-1].goleiro = True

class Jogador:
    def __init__(self, nome) -> None:
        self.nome = nome
        self.gols = 0
        self.forca = random.randint(50, 100)
        self.goleiro = False

class Partida:
    def __init__(self, time1, time2) -> None:
        self.time1 = time1
        self.time2 = time2
        self.gols_time1 = 0
        self.gols_time2 = 0
        self.vencedor = None

    def simula(self):
        probabilidade_empate = 0.15 * (self.time1.forca + self.time2.forca)
        forca_total = self.time1.forca + self.time2.forca + probabilidade_empate

        prob1 = self.time1.forca / forca_total
        prob2 = self.time2.forca / forca_total
        r = random.random()
        if r < prob1:
            self.gols_time2 = random.randint(0, 2)
            self.gols_time1 = random.randint(self.gols_time2 + 1, self.gols_time2 + 2)
            self.vencedor = self.time1
            self.time1.pontos += 3
        elif r < prob1 + prob2:
            self.gols_time1 = random.randint(0, 2)
            self.gols_time2 = random.randint(self.gols_time1 + 1, self.gols_time1 + 2)
            self.vencedor = self.time2
            self.time2.pontos += 3

        else:
            self.gols_time1 = random.randint(0, 3)
            self.gols_time2 = self.gols_time1
            self.vencedor = None
            self.time1.pontos += 1
            self.time2.pontos += 1




class Rodada:
    def __init__(self, partidas, rodada) -> None:
        self.partidas = partidas
        self.rodada = rodada
    
    def simula_automatico(self):
        for p in self.partidas:
            p.simula()
    
    def apresenta_resultados(self):
        print(f"Resultados da rodada {self.rodada}:")
        for p in self.partidas:
            print(f"{p.time1.nome} {p.gols_time1} x {p.gols_time2} {p.time2.nome}")

class Temporada:

    rodadas = []
    numero_rodada = 1

    def __init__(self) -> None:
        self.primeira_metade = True
        with open("times.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
    
        times = []
        for team_data in data.get('teams', []):
            nome_time = team_data.get('name')
            jogadores = [Jogador(j) for j in team_data.get('players', [])]
            time = Time(jogadores, nome_time)
            times.append(time)
        self.times = times
        print("Times criados com sucesso!")
    
    def pareia_times(self):
        pares = list(itertools.combinations(self.times, 2))
    
        i = (self.numero_rodada - 1) * (len(self.times) // 2)
        j = self.numero_rodada * (len(self.times) // 2)
        partidas = []
        for p in pares[i:j]:
            partidas.append(Partida(p[0], p[1]))
        def gerar_combinacoes_ordenadas(todas_combinacoes):
            num_times = len(self.times)
            organizado = []
            while len(organizado) < len(todas_combinacoes):
                for i in range(num_times):
                    for j in range(i + 1, num_times):
                        if (self.numero_rodada + i + j) % 2 == 0:
                            organizado.append((self.times[i], self.times[j]))
            return organizado
        partidas = gerar_combinacoes_ordenadas(partidas)
        return partidas

    def finaliza_temporada(self):
        print("Temporada finalizada!")
        print("Tabela final:")
        self.times.sort(key=lambda x: x.pontos, reverse=True)
        for i, t in enumerate(self.times):
            print(f"{i + 1} - {t.nome} - {t.pontos} pontos")
        exit()
    def simula_rodada(self):
        pares = self.pareia_times()
        rodada = Rodada(pares, self.numero_rodada)
        rodada.simula_automatico()
        rodada.apresenta_resultados()
        self.rodadas.append(rodada)
        self.numero_rodada += 1
        if self.numero_rodada > len(self.times) - 1:
            if self.primeira_metade:
                self.numero_rodada = 1
                self.primeira_metade = False
            else:
                self.finaliza_temporada()
            return

t = Temporada()
while True:
    t.simula_rodada()