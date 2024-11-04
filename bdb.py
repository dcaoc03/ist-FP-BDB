#   Fundamentos da Programacao - Projeto 1: Buggy Data Base (BDB)
#   Diogo Cabral Antunes de Oliveira Costa
#   ist1103179
#   diogo.oliveira.costa@tecnico.ulisboa.pt

#1: Correcao da documentacao
#1.2.1
def corrigir_palavra(palavra):
    '''
    string --> string
    A funcao recebe uma string corrompida e remove todos os pares ordenados \
    minuscula-maiuscula ou maiuscula-minuscula, terminando apenas quando ja 1
    nao existir nenhum desses pares
    '''
    letra = 1
    while letra < len(palavra):
        sub = ord(palavra[letra - 1]) - ord(palavra[letra])
        if abs(sub) == 32:
            palavra = palavra[:letra - 1] + palavra[letra + 1:]
            letra = 1
        else:
            letra += 1
    return(palavra)      


#1.2.2
def eh_anagrama(p1, p2):
    '''
    string, string --> booleano
    Recebe duas strings correspondentes a duas palavras, analisando a lista ordenar
    de cada uma e verifica se tem igual numero de elementos e se todos os seus 
    elementos sao iguais, retornando True se tal acontecer, False se não
    '''
    def ordenar(p):
        '''
        string --> lista
        Recebe uma string e retorna uma lista correspondente aos valores do codigo 
        ASCII de cada carater da string
        Os carateres se forem maiusculos sao associados ao codigo ASCII da sua respetiva
        letra minuscula
        '''
        lista_p = []
        for letra in range(0, len(p)):
            if 96 < ord(p[letra]) < 193:
                lista_p.append(ord(p[letra]))
            if 64 < ord(p[letra]) < 91:
                lista_p.append(ord(p[letra]) + 32)
        return(lista_p)
    
    p1_ordenado, p2_ordenado = sorted(ordenar(p1)), sorted(ordenar(p2))
    letras_comuns = 0
    if len(p1) == len(p2):
        for n in range(0, len(p1_ordenado)):
            if p1_ordenado[n] == p2_ordenado[n]:
                letras_comuns += 1
        if letras_comuns == len(p1) and ordenar(p1) != ordenar(p2):
            return True
        return False
    return False


#1.2.3      
def corrigir_doc(texto):
    '''
    string --> string
    Recebe um texto corrompido da Buggy Data Base e retorna o mesmo texto 'filtrado'
    Primeiro verifica se se trata de um texto valido, retirando os pares de letras repetidas
    de seguida e removendo os anagramas por fim
    '''
    def divisao_palavras(texto):
        '''
        string --> lista
        Recebe um texto e retorna uma lista composta pelas palavras desse texto
        '''
        palavras = []
        i = 0
        while " " in texto:
            while i < len(texto):
                if texto[i] == " ":
                    palavras.append(texto[:i])
                    texto = texto[i+1:]
                    i = 0
                else:
                    i += 1
            palavras.append(texto)
            return(palavras)
    def espacos_corretos(texto):
        '''
        string --> boolean
        Recebe uma cadeia de carateres constituida por varias palavras e verifica
        se nao comeca nem termina com carateres espaco e se as palavras nao se encontram
        separadas por mais do que um espaco, retornando True se assim o for e False 
        caso nao
        '''
        n_espacos, n_espacos_corretos = 0, 0
        for i in range(1, len(texto) - 1):
            if ord(texto[i]) == 32:
                n_espacos += 1
            if ord(texto[i]) == 32 and (64 < ord(texto[i-1]) < 91 or 96 < ord(texto[i-1]) < 123) and (96 < ord(texto[i+1]) < 123 or 64 < ord(texto[i+1]) < 91):
                n_espacos_corretos += 1
        if n_espacos == n_espacos_corretos and (64 < ord(texto[0]) < 91 or 96 < ord(texto[0]) < 123) and (96 < ord(texto[len(texto) - 1]) < 123 or 64 < ord(texto[len(texto) - 1]) < 91):
            return True
        return False
    if type(texto) != str or len(texto) < 1:
        raise  ValueError("corrigir_doc: argumento invalido")
    for i in range(0, len(texto)):
        if not(ord(texto[i]) == 32 or 64 < ord(texto[i]) < 91 or 96 < ord(texto[i]) < 123) or not(espacos_corretos(texto)):
            raise ValueError("corrigir_doc: argumento invalido")   
    correcao = corrigir_palavra(texto)
    texto_final = ""
    palavras = divisao_palavras(correcao)
    n, p = 0, 1    
    while n < (len(palavras) - 1):
        while p < len(palavras):
            if (eh_anagrama(palavras[n], palavras[p])):
                palavras = palavras[:p] + palavras[p+1:]
                p = n + 1
            else:
                p += 1
        n += 1
        p = n + 1
    for i in range(0, len(palavras) - 1):
        texto_final += str(palavras[i]) + " " 
    texto_final += str(palavras[len(palavras) - 1])
    return(texto_final)
        



#2: Descoberta do PIN
#2.2.1
def obter_posicao(letra, num):
    '''
    cadeia de carateres, inteiro --> inteiro
    Recebe um dos carateres 'C', 'B', 'E' ou 'D' e um digito de 1 a 9 correspondente
    a uma posicao painel de botoes quadrado 3x3, a funcao retorna a nova posicao
    apos se desclocar uma para cima, baixo, esquerda ou direita, de acordo com
    o carater ser 'C', 'B', 'E' ou 'D', respetivamente. Se nao for 
    possivel fazer o moviemnto na tecla em que se encontra, a posicao mantem-se 
    igual
    '''
    if letra == "C":
        if num >= 4 and num <= 9:
            num -= 3
    if letra == "B":
        if num >= 1 and num <= 6:
            num += 3
    if letra == "E":
        if num in (2, 3, 5, 6, 8, 9):
            num -= 1
    if letra == "D":
        if num in (1, 2, 4, 5, 7, 8):
            num += 1
    return(num)


#2.2.2
def obter_digito(movimentos, num):
    '''
    cadeia de carateres, inetiro --> inteiro
    Recebe uma cadeia de carateres composta pelas letras 'C', 'B', 'E' e 'D' e
    uma posicao inicial num painel com os digitos de 1 a 9 dispostos num quadrado
    de 3x3. A letra 'C' indica move a posição uma tecla para cima, a 'B' move uma
    para baixo, a 'E' uma para a esquerda e a 'D' uma para a direita. 
    '''    
    for x in range(0, len(movimentos)):
        num = obter_posicao(movimentos[x], num)
    return(num)


#2.2.3
def obter_pin(inst):
    '''
    tuplo --> tuplo
    Recebe um tuplo com entre 4 e 10 combinacoes das letras 'C, 'B', 'E' e/ou 'D' e
    retorna um tuplo com as novas posicoes no mesmo teclado das funcoes anteriores
    que vai assumindo, comacando ao inico na posicao 5
    '''
    res = ()
    if type(inst) != tuple or len(inst) < 4 or len(inst) > 10:
        raise ValueError("obter_pin: argumento invalido")
    for i in range(0, len(inst)):
        if type(inst[i]) != str or len(inst[i]) == 0:
            raise ValueError("obter_pin: argumento invalido")
        for n in range(0, len(inst[i])):
            if inst[i][n] not in ('C', 'B', 'E', 'D'):
                raise ValueError("obter_pin: argumento invalido")
    digito = obter_digito(inst[0], 5)
    res += (digito,)
    if len(inst) > 1:
            for n in range(1, len(inst)):
                res += (obter_digito(inst[n], digito),)
                digito = obter_digito(inst[n], digito)
    return(res)
        



#3: Verificacao de dados
#3.2.1 / 4.2.1
def eh_entrada(entrada):
    '''
    universal --> boolean
    Recebe uma entrada qualquer e retorna True se receber um tulpo com 3 campos:
    uma cadeia de carateres constituida por uma ou mais palavras constituidas por
    letras minusculas e separadas por tracos, uma cadeia de carateres constituidas
    por cinco letras minusculas englobadas por '[' e ']' e um tuplo constiuido
    por dois ou mais numeros inteiros positivos. Retorna False em qualquer outra
    situacao.
    '''
    def tracos_corretos(texto):
        '''
        string --> boolean
        Recebe uma cadeia de carateres constituida por varias palavras e verifica
        se nao comeca nem termina com carateres traco e se as palavras nao se encontram
        separadas por mais do que um traco, retornando True se assim o for e False 
        caso nao
        '''
        n_tracos, n_tracos_corretos = 0, 0
        for i in range(1, len(texto) - 1):
            if ord(texto[i]) == 45:
                n_tracos += 1
            if ord(texto[i]) == 45 and (64 < ord(texto[i-1]) < 91 or 96 < ord(texto[i-1]) < 123) and (96 < ord(texto[i+1]) < 123 or 64 < ord(texto[i+1]) < 91):
                n_tracos_corretos += 1
        if n_tracos == n_tracos_corretos and (64 < ord(texto[0]) < 91 or 96 < ord(texto[0]) < 123) and (96 < ord(texto[len(texto) - 1]) < 123 or 64 < ord(texto[len(texto) - 1]) < 91):
            return True
        return False    
    p1, p2, p3 = 0, 0, 0
    if type(entrada) == tuple and len(entrada) == 3:
        checksum, controlo, seg = entrada[0], entrada[1], entrada[2]
        if type(checksum) == str and tracos_corretos(checksum):
            for i in range(0, len(checksum)):
                if (96 <ord(checksum[i])< 123 or ord(checksum[i]) == 45):
                    p1 += 1
        if type(controlo) == str and len(controlo) == 7 and controlo[0] == "[" and controlo[6] ==  "]":
            for j in range(1, 7):
                if (96 < ord(controlo[j]) < 123):
                    p2 += 1
        if type(seg) == tuple and len(seg) >= 2:
            for k in range(0, len(seg)):
                if type(seg[k]) == int and seg[k] > 0:
                    p3 += 1
        if (p1 > 0 and p3 > 0) and p1 == len(checksum) and p2 == 5 and p3 == len(seg):
            return True
        else:
            return False
    else:
        return False


#3.2.2
def validar_cifra(cifra, controlo):
    '''
    cadeia de carateres, cadeia de carateres --> boolean
    Recebe duas cadeia de carateres (a cifra e a cadeia de controlo) e retorna True
    se e so se se a na cifra estieverem pelo menos todos os carateres do controlo, se 
    o primeiro carater do controlo for o que aparece mais vezes na cifra, o segundo carater
    for o segundo mais comum em termos de aparicoes na cifra e assim sucessivamente. Em caso
    de igual numero de aparicoes entre carateres diferentes, o empate e considerado valido.
    Em qualquer outra situacao retorna False.
    '''    
    def conta_carateres(string):
        '''
        string --> dicionario
        Recebe uma string e retorna um dicionario cujas keys sao os carateres da string
        e o value de cada key e o numero de vezes que esse carater especifico aparece
        na string
        '''
        contador = {}
        for i in range(0, len(string)):
            if 96 < ord(string[i]) < 123:
                if string[i] not in contador:
                    contador[string[i]] = 1
                else:
                    contador[string[i]] += 1
        return(contador)
    ocorrencias = conta_carateres(cifra)
    valores_ocorrencias = list(ocorrencias.values())
    certas = 0
    for i in range(1, len(controlo) - 1):
        if controlo[i] not in cifra:
            return False
    for i in range(1, len(controlo) - 1):
        if ocorrencias[controlo[i]] == max(valores_ocorrencias):
            for j in range(i + 1, len(controlo) - 1):
                if ocorrencias[controlo[i]] == ocorrencias[controlo[j]] and ord(controlo[j]) < ord(controlo[i]):
                    return False
            certas += 1
            valores_ocorrencias.remove(max(valores_ocorrencias))
    if certas == 5:
        return True
    else:
        return False


#3.2.3
def filtrar_bdb(lista):
    '''
    lista --> lista
    Recebe uma lista contendo diversas entradas da bdb, verificando primeiro se a entrada
    nao se trata de uma lista vazia ou se um dos seus elementos retorna False na funcao
    eh_entrada, verificando de seguida se algum dos elementos da entrada retorna False
    na funcao validar_cifra (ou seja, se a sua senha nao seguir as regras definidas).
    No final retorna a lista contendo apenas os elementos que retornaram True em eh_entrada
    e False em validar_senha.
    '''
    if type(lista) != list or len(lista) == 0:
        raise ValueError("filtrar_bdb: argumento invalido")
    i = 0
    while i < len(lista): 
        if not(eh_entrada(lista[i])):
            raise ValueError("filtrar_bdb: argumento invalido")
        if validar_cifra(lista[i][0], lista[i][1]):
            lista.remove(lista[i])
            i = 0
        else:
            i += 1
    return(lista)




#4: Desencriptacao de dados
#4.2.2
def obter_num_seguranca(valores):
    '''
    tuplo --> inteiro
    Recebe um tuplo constituido por dois ou mais numeros inteiros positivos e
    retorna a menor diferenca possivel entre um par de elementos
    '''
    diferencas_positivas = []
    for n in range(0, len(valores) - 1):
        for m in range(n + 1, len(valores)):
            diferencas_positivas.append(abs(valores[n] - valores[m]))
    return(min(diferencas_positivas))


#4.2.3
def decifrar_texto(cifra, num_seguranca):
    '''
    cadeia de carateres, inteiro --> cadeia de carateres
    Recebe uma cadeia de carateres (a cifra) e um inteiro (seguranca) e retorna a cifra
    descodificada da seguinte maneira: cada letra da cifra avanca um numero de vezes
    no alfabeto igual a seguranca, avancando mais uma posicao de o carater ocupar uma
    posicao par na string ou recuando uma caso oucupe uma posicao impar. Os tracos
    sao transformados em espacos durante a descodificacao.
    '''
    codigo_decifrado = ""
    for i in range(0, len(cifra)):
        num_seguranca2 = num_seguranca
        if cifra[i] == "-":
            codigo_decifrado += " "
        else:
            n = ord(cifra[i])
            while num_seguranca2 > (ord("z") - n):
                num_seguranca2 -= (ord("z") - n) + 1
                n = ord("a")
            letra = n + num_seguranca2
            if i % 2 == 0:
                if chr(letra) == "z":
                    codigo_decifrado += "a"
                else:
                    codigo_decifrado += chr(n + num_seguranca2 + 1)
            else:
                if chr(letra) == "a":
                    codigo_decifrado += "z"
                else:
                    codigo_decifrado += chr(n + num_seguranca2 - 1)
    return(codigo_decifrado)


#4.2.4
def decifrar_bdb(dados):
    '''
    lista --> lista
    Recebe uma lista contendo varias possiveis entradas, verificando primeiro se cada
    entrada retorna True na funcao eh_entrada, procedendo a descodicacao segundo a 
    funcao decifrar_texto e usando como numero de seguranca o resultado da funcao 
    obter_num_seguranca. No fim retorna a lista com as entradas descodificadas pela
    mesma ordem da lista inicial.
    '''
    res = []
    for i in range(0, len(dados)):
        if type(dados) != list or not(eh_entrada(dados[i])):
            raise ValueError("decifrar_bdb: argumento invalido")
        num = obter_num_seguranca(dados[i][2])
        res.append(decifrar_texto(dados[i][0], num))
    return(res)




#5: Depuracao de senhas
#5.2.1
def eh_utilizador(arg):
    '''
    universal --> boolan
    Recebe um argumento universal e retorna True apenas se se tratar de um utilizador da bdb:
    se o argumento for um dicionario com a entrada 'name' correspondente a uma cadeia de carateres,
    a entrada 'pass' correspondente a outra cadeia de carateres e a entrada 'rule' correspondente a 
    outro dicionario com dois argumentos, o primeiro 'vals' e um tuplo com dois numeros inteiros positivos
    com o segundo maior que o primeiro e o segundo 'char' corresponde a uma letra minuscula
    '''
    def verifica_regras(regra):
        '''
        dicionario --> boolean
        Recebe um dicionario contendo duas keys: 'vals' e 'char', correspondentes as regras individuais
        da senha de cada utilizador da bdb. A key 'vals' e um tuplo com dois valores, o segundo maior
        que o primeiro, que indica o minimo e maximo numero de vezes que o carater indicado em 'char'
        pode aparecer na password.
        '''
        vals, char = regra['vals'], regra['char']
        if type(vals) == tuple and type(char) == str:
            if len(vals) == 2 and len(char) == 1:
                if type(vals[0]) == type(vals[1]) == int and vals[0] > 0 and vals[1] > 0 and (96 < ord(char[0]) < 123):
                    if vals[0] <= vals[1]:
                        return True
        return False
    if isinstance(arg, dict) and len(arg) == 3:
        nome, passw, regra = arg['name'], arg['pass'], arg['rule']
        if type(nome) == str and len(nome) >= 1:
            if type(passw) == str and len(passw) >= 1:
                if type(regra) == dict and len(regra) == 2 and verifica_regras(regra):
                    return True
    return False


#5.2.2
def eh_senha_valida(senha, regra):
    '''
    string, dicionario --> boolenan
    Recebe uma string correspondente a uma password e um dicionario correspondente
    a regra da password. Para retornar True, a password precisa de cumprir tanto as
    regras gerais como a especifica. As regras gerais correspondem a ter pelo menos
    tres carateres iguais a vogais minusculas e ter pelo menos um carater que apareca
    duas vezes consecutivas. A regra particular corresponde a o carater defindo na
    entrada 'char' aparecer um minimo numero de vezes na password igual ao primeiro
    elemento do tuplo 'vals' e um maximo numero de vezes igual ao segundo elemento
    desse tuplo. Em caso contrario, retorna false.
    '''
    n_vogais, letras_repetidas = 0, 0
    for n in range(0, len(senha)):
        if senha[n] in ('a', 'e', 'i', 'o', 'u'):
            n_vogais += 1
        if n >= 1:
            if senha[n] == senha[n-1]:
                letras_repetidas += 1
    if n_vogais >= 3 and letras_repetidas >= 1:
        n_char = 0
        for j in range(0, len(senha)):
            if senha[j] == regra['char']:
                n_char += 1
        if regra['vals'][0] <= n_char <= regra['vals'][1]:
            return True
    return False


#5.2.3
def filtrar_senhas(dados):
    '''
    lista --> lista
    Recebe uma lista contendo varios utilizadores da bdb, verificando se cada elemento
    retorna True na funcao eh_utilizador, caso contrario da erro. Se um utilizador
    dessa lista tiver uma senha que nao e valida, o nome do utilizador e adicionado
    a lista de respostas que e retornada apos percorrer todos os elementos da lista.
    No final, a lsta e retornada por ordem alfabetica.
    '''
    lista_nomes = []  
    if type(dados) != list or len(dados) < 1:
        raise ValueError('filtrar_senhas: argumento invalido')
    for utilizador in dados:    
        if not(eh_utilizador(utilizador)):
            raise ValueError('filtrar_senhas: argumento invalido')
        if not eh_senha_valida(utilizador['pass'], utilizador['rule']):
            lista_nomes.append(utilizador['name'])
    return(sorted(lista_nomes))