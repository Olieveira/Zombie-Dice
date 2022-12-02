# NOME: NATHAN DE OLIVEIRA DE MELO

import random
import os
import time

# variaveis
partida_rodando = True
# dados
verde = ['C', 'P', 'C', 'T', 'P', 'C']
amarelo = ['T', 'P', 'C', 'T', 'P', 'C']
vermelho = ['T', 'P', 'T', 'C', 'P', 'T']
# tubo padrão
tubo_dos_jogadores = [verde, verde, verde, verde, verde, verde, amarelo, amarelo, amarelo, amarelo, vermelho, vermelho,
                      vermelho]
# contadores
cerebros_da_rodada = 0
rodadas = 0
quantidade_jogadores = 0
ultimo_vencedor = -1
jogador_da_vez = -1
# jogadores e respectivos contadores
jogadores = []
tiros_levados = []
cerebros_comidos = []
passos = []
dados_sorteados = []

# limpa o terminal
os.system('cls')

# sorteia os dados
def sorteia_dados():
    """
    Sorteia os 3 dados do tubo. Se possuir dados com faces 'passos' da rodada anterior, re-sorteia os mesmos ao invés de retirar outro do tubo.

    """
    global dados_sorteados
    global tubo_dos_jogadores
    global cerebros_comidos
    global tiros_levados
    global passos
    global cerebros_da_rodada
    global jogador_da_vez
    global verde
    global vermelho
    global amarelo

    # sortea 3 dados do tubo
    for j in range(len(dados_sorteados), 3):
        if len(dados_sorteados) >= 3: # se ja foram sorteados 3 dados
            break # sai do loop
        else:
            dado_girado = random.choice(tubo_dos_jogadores) # sorteia um dado do tubo

            # verifica a cor do dados sorteado, adiciona-o na lista dos dados sorteados e sorteia a face
            if dado_girado == verde:
                dados_sorteados.append({"cor": verde, "face": random.choice(verde)})
                tubo_dos_jogadores.remove(verde)
            elif dado_girado == vermelho:
                dados_sorteados.append({"cor": vermelho, "face": random.choice(vermelho)})
                tubo_dos_jogadores.remove(vermelho)
            elif dado_girado == amarelo:
                dados_sorteados.append({"cor": amarelo, "face": random.choice(amarelo)})
                tubo_dos_jogadores.remove(amarelo)
            # verifica a face sorteada e contabiliza na respectiva variavel do respectivo jogador
            if dados_sorteados[j]["face"] == "C":
                cerebros_comidos[jogador_da_vez]["quantidade"] += 1
                cerebros_da_rodada += 1
                cerebros_comidos[jogador_da_vez]["cor"] = dados_sorteados[j]["cor"]
            elif dados_sorteados[j]["face"] == "P":
                passos[jogador_da_vez]["quantidade"] += 1
                passos[jogador_da_vez]["cor"] = dados_sorteados[j]["cor"]
            elif dados_sorteados[j]["face"] == "T":
                tiros_levados[jogador_da_vez]["quantidade"] += 1
                tiros_levados[jogador_da_vez]["cor"] = dados_sorteados[j]["cor"]

    faces = convert_background(dados_sorteados) # estiliza os dados com o fundo de sua respectiva cor com com código ANSI

    cores = filtra_cores(tubo=tubo_dos_jogadores) # conta quantos dados de cada cor tem no tubo

    # limpa o terminal e imprime o cabeçalho padrão
    default_layout(state=True, nome=jogadores[jogador_da_vez], tiros=tiros_levados[jogador_da_vez]["quantidade"],
                   passo=passos[jogador_da_vez]["quantidade"], cerebros=cerebros_comidos[jogador_da_vez]["quantidade"],
                   tubo=len(tubo_dos_jogadores), amarelos=cores["amarelo"], verdes=cores["verde"],
                   vermelhos=cores["vermelho"], last_dices=faces)

    # Printa os dados sorteados
    print("\t\033[1;35mDADOS SORTEADOS:\033[0;0m")
    print("\t{} | {} | {}".format(dados_sorteados[0]["face"],
                                  dados_sorteados[1]["face"],
                                  dados_sorteados[2]["face"]).replace("C",
                                                                      "\033[1;32mCÉREBRO\033[0;0m").replace(
        "T",
        "\033[1;31mTIRO\033[0;0m").replace(
        "P", "\033[1;33mPASSOS\033[0;0m"))


# passa para o próximo jogador e contabiliza as variáveis
def next_player(motivo):
    """
    Passa para o próximo jogador contabilizando as respectivas variáveis conforme o motivo da passagem.

    :param motivo: ("tiro" || "passou" || "sem dados") Motivo pelo qual está passando para o próximo jogador
    """
    global jogador_da_vez
    global tiros_levados
    global passos
    global cerebros_comidos
    global cerebros_da_rodada
    global tubo_dos_jogadores
    global dados_sorteados

    # zera as variaveis que não são contabilizadas quando ha troca de turno
    tiros_levados[jogador_da_vez]["quantidade"] = 0
    passos[jogador_da_vez]["quantidade"] = 0
    dados_sorteados.clear()
    tubo_dos_jogadores.clear()
    tubo_dos_jogadores = [verde, verde, verde, verde, verde, verde, amarelo, amarelo, amarelo, amarelo,
                          vermelho, vermelho,
                          vermelho]

    print("\t\033[1;31m--------------------------------------------------------------\033[0;0m")

    # se o jogador tomou 3 tiros
    if motivo == "tiro":
        print(
            "\t\033[1;31m|\033[0;0m\t\033[1;35m{}\033[0;0m \033[0;31mLEVOU 3 TIROS E PERDEU OS \033[1;32m{} CÉREBROS\033[0;0m \033[0;31mDESSA RODADA!!!\033[0;0m".format(
                jogadores[jogador_da_vez],
                cerebros_da_rodada))
        cerebros_comidos[jogador_da_vez]["quantidade"] -= cerebros_da_rodada # Subtrai os cérebros obtidos no turno

    # se o jogador optou passar a vez
    elif motivo == "passou":
        print(
            "\t\033[1;31m|\033[0;0m\t\033[1;35m{}\033[0;0m passou a vez e já comeu \033[1;32m{} CÉREBROS!!!\033[0;0m".format(
                jogadores[jogador_da_vez],
                cerebros_comidos[
                    jogador_da_vez][
                    "quantidade"]))
    # se acabou os dados do tubo do jogador
    elif motivo == "sem dados":
        print(
            "\t\033[1;31m|\033[0;0m\t\033[1;35m{}\033[0;0m \033[0;31mnão possui dados suficientes no tubo para mais uma rodada!!!\033[0;0m".format(
                jogadores[jogador_da_vez]))
        print(
            "\t\033[1;31m|\033[0;0m\t\033[1;31mPassou a vez e pontuou\033[0;0m \033[1;32m{} CÉREBROS!!\033[0;0m".format(
                cerebros_comidos[jogador_da_vez]["quantidade"]))

    print("\t\033[1;31m--------------------------------------------------------------\033[0;0m\n")
    print("\t\033[1;31m==============PASSANDO A VEZ==============\033[0;0m")
    
    time.sleep(3)

    # indica o próximo jogador
    if jogador_da_vez >= len(jogadores) - 1: # se for o ultimo jogador
        jogador_da_vez = 0
    else:
        jogador_da_vez += 1

    cerebros_da_rodada = 0

    # limpa o terminal e imprime o cabeçalho padrão
    default_layout(state=True, nome=jogadores[jogador_da_vez],
                   tiros=tiros_levados[jogador_da_vez]["quantidade"],
                   passo=passos[jogador_da_vez]["quantidade"],
                   cerebros=cerebros_comidos[jogador_da_vez][
                       "quantidade"])  # limpa o console e printa novamente


# estiliza o fundo dos dados com sua respectiva cor por meio de código ANSI
def convert_background(dados):
    """
        Converte o fundo dos dados passados como parâmetro para sua respectiva cor
    
    :param dados: Array contendo dicionários com os dados sorteados e suas respectivas faces. list[dict["cor": x, "quant": y], ...]
    :return: Retorna o array com os valores estilizados por meio de código ANSI
    """

    global verde
    global amarelo
    global vermelho
    resposta = []

    for j in dados:
        if j["cor"] == verde:
            resposta.append("\033[1;31;42m   {}   \033[0;0m".format(j["face"]))
        elif j["cor"] == amarelo:
            resposta.append("\033[1;31;43m   {}   \033[0;0m".format(j["face"]))
        elif j["cor"] == vermelho:
            resposta.append("\033[1;31;41m   {}   \033[0;0m".format(j["face"]))

    return resposta


# faz a contagem dos dados de cada cor do tubo
def filtra_cores(tubo):
    """
    Faz a contagem dos dados amarelo, vermelho e verde do tubo

    :param tubo: Array contendo os dados que estão no tubo
    :return: Retorna um dicionário com a contagem de cada cor. {"verde": x, "amarelo": y, "vermelho": z}
    """

    global verde
    global amarelo
    global vermelho
    vd = 0
    am = 0
    vm = 0

    for j in tubo:
        if j == verde:
            vd += 1
        elif j == amarelo:
            am += 1
        elif j == vermelho:
            vm += 1

    return {"verde": vd, "amarelo": am, "vermelho": vm}


# printa as informações do jogo
def default_layout(state, nome='', tiros=0, passo=0, cerebros=0, tubo=13, amarelos=4, verdes=6, vermelhos=3,
                   last_dices=None):
    """
    Limpa as informações anteriores e exibe o cabeçalho padrão e as informações atuais do progresso do jogo

    :param state: Boleano, Representa o início do jogo
    :param nome:  Str, Nome do jogador atual
    :param tiros: Int, Quantidade de tiros do jogador atual
    :param passo: Int, Quantidade de passos do jogador atual
    :param cerebros: Int, Quantidade de cerebros do jogador atual
    :param tubo: Array, Tubo com os dados do jogador da vez
    :param amarelos: Int, Quantidade de dados amarelos no tubo
    :param verdes: Int, Quantidade de dados verdes no tubo
    :param vermelhos: Int, Quantidade de dados vermelhos no tubo
    :param last_dices: Array, Contém os últimos dados sorteados
    """
    os.system('cls')

    # se o jogo ainda não iniciou
    if not state:
        print("\n\t\033[1;32m==========================================================")
        print("\t=====================\033[1;31m ZOMBIE DICE \033[0;0m\033[1;32m========================")
        print("\t==========================================================\033[0;0m\n")
    else:
        print("\n\t\033[1;31m|======================================================")
        print("\t| \t\033[1;32mINFORMAÇÕES DO JOGADOR\033[1;0m \033[1;35m{}: \033[0;0m".format(nome))
        print("\t\033[1;31m|\033[0;0m")
        print(
            "\t\033[1;31m| \033[1;31mTIROS: \033[1;35m{} \t\033[1;33mPASSOS: \033[1;35m{}\t\033[1;32mCÉREBROS:\033[0;35m {} ".format(
                tiros, passo, cerebros))
        print("\t\033[1;31m|\033[0;0m")
        # se possui ultimos dados
        if last_dices is not None:
            print(
                "\t\033[1;31m| \033[1;34mDADOS NO TUBO: \033[1;35m{} \t\033[1;34mÚLTIMOS DADOS SORTEADOS:".format(
                    tubo))
            print("\t\033[1;31m| \033[1;3;41m  {}  \033[1;43m  {}  \033[1;42m  {}  \033[0;0m\t{}|{}|{}".format(
                vermelhos, amarelos,
                verdes, last_dices[0], last_dices[1], last_dices[2]))

        else:
            print(
                "\t\033[1;31m| \033[1;34mDADOS NO TUBO: \033[1;35m{} \t\033[0;0m".format(tubo))
            print(
                "\t\033[1;31m| \033[1;31;41m  {}  \033[1;43m  {}  \033[1;42m  {}  \033[0;0m".format(vermelhos,
                                                                                                    amarelos,
                                                                                                    verdes))
        print("\t\033[1;31m|======================================================\033[0;0m\n")


default_layout(state=False)

# enquanto não for informado uma quantidade suficiente de jogadores
while quantidade_jogadores <= 1:
    try:
        quantidade_jogadores = int(input("\tQuantos jogadores irão participar? ")) # pergunta quantidade de jogadores e converte
        if quantidade_jogadores <= 1: # se foi informado menos que 2
            print("\n\tÉ necessário no mínimo 2 jogadores!")
    except ValueError:
        print("\n\tValor informado inválido!")
        quantidade_jogadores = 0

# pede o nome de cada um dos jogadores e cria um index nas listas para cada jogador
for i in range(quantidade_jogadores):
    jogadores.append(input("\n\tInsira o nome do jogador de n°{}: ".format(i + 1)).upper())
    tiros_levados.append({"quantidade": 0, "cor": ""})
    cerebros_comidos.append({"quantidade": 0, "cor": ""})
    passos.append({"quantidade": 0, "cor": ""})

# printa uma lista com o nome dos jogadores e seu respectivo n°
print("\n\tJOGADORES PARTICIPANDO(\033[1;32m{}\033[0;0m):".format(len(jogadores)))
for i in range(quantidade_jogadores):
    print("\t{} - \033[1;35m{}\033[0;0m".format(i + 1, jogadores[i]))

# define quem começara a partida
if ultimo_vencedor >= 0:
    print("\n\tO {} começará pois venceu a última partida!".format(jogadores[ultimo_vencedor]))
    jogador_da_vez = ultimo_vencedor
else:
    escolha = 0
    while jogador_da_vez < 0: # enquanto não for escolhido uma forma válida para definir o primeiro jogador
        try:
            escolha = int(input("\n\tEscolha o n° de uma opção para definir o primeiro jogador!\n\t"
                                "(\033[1;35m1\033[0;0m)Escolha aleatória\n\t"
                                "(\033[1;35m2\033[0;0m)Escolha manual\n\t"
                                "--> "))
        except ValueError:
            print("\tValor inválido!")

        if escolha == 1: # se foi escolhido de forma aleatória
            jogador_da_vez = random.randint(0, len(jogadores) - 1)
            print("\n\t\033[1;32m{}\033[0;0m foi o(a) sortudo(a) da vez e iniciará a partida!".format(
                jogadores[jogador_da_vez]))
        elif escolha == 2: # se foi escolhido de forma manual
            id_tipo = None
            try: # pede o nome ou numero do jogador informado
                jogador_da_vez = input(
                    "Insira o \033[1;32mn°\033[0;0m ou \033[1;32mnome\033[0;0m do jogador que começará: ")
                jogador_da_vez = int(jogador_da_vez)
                id_tipo = int
            except ValueError: # se der erro foi informado o nome e não numero
                id_tipo = str

            # verifica se o valor informado equivale ao n° ou nome de algum dos jogadores
            for i in range(quantidade_jogadores):

                # se o valor informado foi um int
                if id_tipo is int:
                    if i + 1 == jogador_da_vez:
                        jogador_da_vez -= 1
                        print("\tO jogador \033[1;35m{}\033[0;0m iniciará a partida!".format(jogadores[i]))
                        break
                    else:
                        if i == quantidade_jogadores:
                            print("\tO jogador informado n existe!")

                # se o valor informado foi uma string
                elif id_tipo is str:
                    if jogadores[i].upper() == jogador_da_vez.upper():
                        jogador_da_vez = i
                        print("\t\033[1;35m{}\033[0;0m iniciará a partida!".format(jogadores[i]))
                        break
                    else:
                        if i == quantidade_jogadores - 1:
                            print("\tO jogador informado não existe!")
                            jogador_da_vez = -1

# limpa o terminal e imprime o cabeçalho padrão
default_layout(state=True, nome=jogadores[jogador_da_vez])

while partida_rodando: # enquanto a partida estiver rodando
    input("\t\033[1;35m{},\033[0;0m pressione uma tecla para girar os dados: ".format(jogadores[jogador_da_vez]))

    sorteia_dados() # função que sorteia os dados até completar 3

    # verifica possíveis fins de turno e/ou jogo

    # se tomou 3 tiros
    if tiros_levados[jogador_da_vez]["quantidade"] >= 3:
        next_player("tiro")

    # se comeu 13 cerebros e venceu
    elif cerebros_comidos[jogador_da_vez]["quantidade"] >= 13:
        print(
            "\n\t\033[1;32mPARABÉNS \033[1;35m{}\033[0;0m\033[1;32m, VOCÊ COMEU 13 CÉREBROS E VENCEU A PARTIDA!!".format(
                jogadores[jogador_da_vez]))
        ultimo_vencedor = jogadores[jogador_da_vez]
        partida_rodando = False

    # se não possui dados suficiente para continuar
    elif len(tubo_dos_jogadores) + passos[jogador_da_vez]["quantidade"] < 3:
        next_player("sem dados")

    else:
        continuar = ''
        while continuar != "S" and continuar != "N": # enquanto não for informado se deseja ou não continuar
            continuar = input(
                "\n\t\033[1;35m{}\033[0;0m, deseja continuar seu turno? (\033[1;32mS\033[0;0m ou \033[1;31mN\033[0;0m) ".format(
                    jogadores[jogador_da_vez])).upper()

            # se o jogador desejar continuar
            if continuar == "S" or continuar == "s":

                # RE-SORTEIA OS DADOS DE PASSOS E SOMA NAS RESPECTIVAS VARIAVEIS
                verified = False
                indice = 0
                passos[jogador_da_vez]["quantidade"] = 0

                while not verified: # enquanto os dados passos não forem verificados
                    if indice >= len(dados_sorteados):
                        verified = True
                    else:
                        if dados_sorteados[indice]["face"] != "P": # se a face é diferente de passos
                            del dados_sorteados[indice] # deleta o dado da lista de dados sorteados
                        else: # se for de face passos
                            dados_sorteados[indice]["face"] = random.choice(dados_sorteados[indice]["cor"]) # mantém o dado e re-sorteia conforme sua cor

                            # verifica a face sorteada e contabiliza nas respectivas variáveis
                            if dados_sorteados[indice]["face"] == 'P':

                                passos[jogador_da_vez]["quantidade"] += 1

                            elif dados_sorteados[indice]["face"] == 'C':

                                cerebros_comidos[jogador_da_vez]["quantidade"] += 1
                                cerebros_da_rodada += 1

                            elif dados_sorteados[indice]["face"] == 'T':

                                tiros_levados[jogador_da_vez]["quantidade"] += 1

                            indice += 1 # controlador do loop

                print("\n\tReutilizando {} dados de passos e {} dados do tubo para complementar 3 dados!\n".format(
                    len(dados_sorteados),
                    3 - len(
                        dados_sorteados)))

                time.sleep(2)

            # se o jogador não quiser jogar novamente então contabiliza seus pontos e restaura seu tubo
            elif continuar == "N" or continuar == "n":
                next_player("passou") # passa para o próximo jogador especificando o motivo
            else:
                print("\tValor inválido, insira novamente!\n")
