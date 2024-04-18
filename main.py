import csv

def menuDeOpcoes():
    print("1 - Carregar dados do arquivo")
    print("2 - Listar todos os dados")
    print("3 - Preço médio do abacate em cada região")
    print("4 - A data em que foi observado o maior preço")
    print("5 - Tipo de abacate que tem maior preço médio")
    print("6 - Inserir novo preco")
    print("7 - Digite uma regiao para saber a variacao percentual do ano mais antigo em relacao ao atual")
    print("8 - Para descobrir o mês em que o preço é mais caro em cada região.")
    print("9 - Para o preço médio do abacate no ano e mês")
    print("10 - Para a diferença média de preço entre os abacates “convencionais” e “orgânicos”")
    print("11 - Criar um novo arquivo com maior preço praticado em cada região")
    print("12 - Para saber o ano em que mais abacates foram vendidos")
    print("13 - Qual preco medio do abacate organico em todo tempo de analise")

def validarMenu(opcao):
    while opcao < 0 or opcao > 13:
        print(">> Inválido. Tente novamente!\n")
        menuDeOpcoes()
        opcao = int(input("Escolha uma opção ou 0 para sair: "))
    return opcao

def abrirArquivo(arqv):
    mat = []
    arqv = open(arqv, "r")

    for linha in arqv:
        linha = linha.replace("\n", "")
        linha = linha.split(",")
        if linha[0] == "Date":
            continue
        mat.append(linha)
    arqv.close()
    return mat

def listarDados(mat):
    print("Listar arquivo:")
    for linha in mat:
        print(linha)

def precoMedioRegiao(mat):
    print("Preco medio dos abacates por regiao!")

    DicVal = {}
    DicQtd = {}

    for linha in mat:
        valor = float(linha[2])
        regiao = linha[-1]

        if regiao not in DicVal:
            DicVal[regiao] = valor
            DicQtd[regiao] = 1
        else:
            DicVal[regiao] += valor
            DicQtd[regiao] += 1

    for regiao, valor in DicVal.items():
        media = valor / DicQtd[regiao]
        print(f'{regiao}: {media:.3f}')

def TipoMaiorPrecoMedio(mat):
    DicQtdTipo = {}
    DicVal = {}

    for linha in mat:
        valor = float(linha[2])
        tipo = linha[11]

        if tipo not in DicVal:
            DicVal[tipo] = valor
            DicQtdTipo[tipo] = 1
        else:
            DicVal[tipo] += valor
            DicQtdTipo[tipo] += 1

    tipoMaiorMedia = ""
    MaiorMedia = 0
    for tipo, valor in DicVal.items():
        media = valor / DicQtdTipo[tipo]

        if media > MaiorMedia:
            MaiorMedia = media
            tipoMaiorMedia = tipo

    return tipoMaiorMedia, MaiorMedia

def dataMaiorPreco(mat):
    maiorPreco = float(mat[0][2])
    data = mat[0][1]

    for linha in mat:
        if maiorPreco > float(linha[2]):
            maiorPreco = float(linha[2])
            data = linha[1]

    return data

def novoAbacate(mat, arqv):
    print("Adic. ou remover entrada no arquivo e em memória:")
    lista = []

    print(">> Digite os dados da nova entrada:")

    tipo = str(input("Qual o nome do tipo do abacate?"))
    valor = float(input("Qual o valor desse tipo de abacate?"))
    regiao = str(input("Qual a regiao das vendas desse tipo de abacate?"))
    sacas = int(input("Qual total de sacas desse abacate foram vendidas?"))

    lista.append(tipo)
    lista.append(valor)
    lista.append(regiao)
    lista.append(sacas)

    opcao = input("\nConfirmar a inserção? (S/N) ")

    if opcao == "S" or opcao == "s":
        print("\n>> Inserção confirmada.")

        with open(arqv, 'a') as file:
            writer_object = csv.writer(file)
            writer_object.writerow(lista)

        mat.append(lista)

    elif opcao == "N" or opcao == "n":
        mat.pop()
        print("\n>> Inserção cancelada.")

def variacaoPercentual(mat):
    precoAntigo = 0
    precoRecente = 0
    anoAntigo = ""
    anoRecente = ""

    regiao = str(input("Em qual regiao voce deseja saber a variacao percentual?"))

    for linha in mat:
        regiaoAtual = linha[-1]
        anoAtual = linha[12]
        precoAtual = float(linha[2])

        if anoAtual > anoRecente:
            anoRecente = anoAtual
            precoRecente = precoAtual

        if anoAtual < anoAntigo or anoAntigo == "":
            anoAntigo = anoAtual
            precoAntigo = precoAtual

    variacaoPercentual = ((precoRecente - precoAntigo) / precoAntigo) * 100

    print(variacaoPercentual)

def retornarMes(dataCompleta):
    dado = dataCompleta.split("-")
    return dado[1]

def maiorPrecoRegiao(mat):
    dicRegiao = {}

    for i in range(len(mat)):
        regiao = mat[i][13]
        if regiao in dicRegiao:
            if float(mat[i][2]) > dicRegiao[regiao][0]:
                dicRegiao[regiao] = float(mat[i][2]), retornarMes(mat[i][1])
        else:
            dicRegiao[regiao] = float(mat[i][2]), retornarMes(mat[i][1])

    for regiao in dicRegiao.keys():
        print(f'O mês em que o preço é mais caro na região {regiao} é o {dicRegiao[regiao][1]}')

def precoMedioMesAno(mat):
    print("Nessa opcao voce escolhe o tipo de abacate, digita mes e ano e te daremos a media de venda do seu tipo")
    contador = 0
    mes_ano = ""
    somaPrecos = 0

    tipo = str(input("Qual tipo de abacate?"))
    ano = int(input("Qual ano voce deseja saber a media?"))
    mes = int(input("Qual mes voce deseja saber a media?"))

    if mes < 10:
        mes_ano = f'{ano}-0{mes}'
    else:
        mes_ano = f'{ano}-{mes}'

    for linha in mat:
        valor = float(linha[2])
        tipoAtual = linha[11]

        if tipoAtual == tipo and mes_ano in linha[1]:
            contador += 1
            somaPrecos += valor

    media = somaPrecos / contador

    print(f"A média no mes e ano {mes_ano} é {media}")

def mediaDiferenca(mat):
    contadorOrganico = 0
    valorOrganico = 0
    contadorConv = 0
    valorConv = 0

    for i in range(len(mat)):
        if mat[i][11] == "organic":
            contadorOrganico += 1
            valorOrganico += float(mat[i][2])
        elif mat[i][11] == "conventional":
            contadorConv += 1
            valorConv += float(mat[i][2])

    if contadorOrganico and contadorConv > 0:
        mediaOrganico = valorOrganico / contadorOrganico
        mediaConv = valorConv / contadorConv

        diferencaOrgConv = (mediaOrganico - mediaConv)

        print(f"A diferenca entre a media de abacates é {diferencaOrgConv}")
        print(f"A quantidade de abacates organicos é {contadorOrganico}")
        print(f"A quantidade de abacates convecional é {contadorConv}")

def anoMaisVendas(mat):
    dicAno = {}

    for i in range(len(mat)):
        ano = mat[i][12]
        volumeTotal = float(mat[i][3])
        if ano not in dicAno:
            dicAno[ano] = volumeTotal
        else:
            dicAno[ano] += volumeTotal

    maiorAno = 0
    maiorVolume = 0
    for ano in dicAno.keys():
        volumeTotal = dicAno[ano]
        if volumeTotal > maiorVolume:
            maiorVolume = volumeTotal
            maiorAno = ano

    print(f"o ano com mais vendas foi o {maiorAno} com o total de {maiorVolume} sacas")

matriz = []
arquivo = "avocado.csv"
opcao = True

while opcao:
    menuDeOpcoes()
    opcao = int(input("Escolha uma opcao ou digite o numero 0 para sair!"))
    opcao = validarMenu(opcao)

    if opcao == 1:
        matriz = abrirArquivo(arquivo)
    elif opcao == 2:
        listarDados(matriz)
        input("Pressione ENTER para continuar!")
    elif opcao == 3:
        precoMedioRegiao(matriz)
    elif opcao == 4:
        dataPreco = dataMaiorPreco(matriz)
        print(dataPreco)
    elif opcao == 5:
        tipoMaior, mediaMaior = TipoMaiorPrecoMedio(matriz)
        print(tipoMaior, mediaMaior)
    elif opcao == 6:
        novoAbacate(matriz, arquivo)
    elif opcao == 7:
        variacaoPercentual(matriz)
    elif opcao == 8:
        maiorPrecoRegiao(matriz)
    elif opcao == 9:
        precoMedioMesAno(matriz)
    elif opcao == 10:
        mediaDiferenca(matriz)
    elif opcao == 12:
        anoMaisVendas(matriz)

