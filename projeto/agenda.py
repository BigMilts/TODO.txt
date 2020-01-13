import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  return(cor + texto + RESET)
  

# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração. 
def adicionar(descricao, extras):
  novaAtividade=''
  #Na maioria dos laços for, o 'i' remete ao indice
  # não é possível adicionar uma atividade que não possui descrição. 
  if descricao  == '' :
    print("erro a descrição da atividade não foi inserida")
    return False
  elif descricao!='':
    if extras!='':
      data=''
      hora=''
      pri=''
      contex=''
      proj=''
      for palavra in extras:
        if dataValida(palavra):
          data+=palavra
        elif horaValida(palavra):
          hora+=palavra
        elif prioridadeValida(palavra):
          pri+=palavra
        elif contextoValido(palavra):
          contex+=palavra
        elif projetoValido(palavra):
          proj+=palavra
      parametros =[data,hora,pri,descricao,contex,proj]
      for parametro in parametros:
        if parametro!='':
          novaAtividade+= parametro +' '
      novaAtividade=novaAtividade.strip()      
          

    else:
      novaAtividade+=descricao

  ################ COMPLETAR


  # Escreve no TODO_FILE. 
  try: 
    fp = open('todo.txt', 'a',encoding='utf-8')
    fp.write(novaAtividade + "\n")
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + 'todo.txt')
    print(err)
    return False

  return True
def manipular(descricao, extras):
  novaAtividade =''
  if descricao  == '' :
    return False
  elif descricao!='':
    if extras!='':
      data=''
      hora=''
      pri=''
      contex=''
      proj=''
      for palavra in extras:
        if dataValida(palavra):
          data+=palavra
        elif horaValida(palavra):
          hora+=palavra
        elif prioridadeValida(palavra):
          pri+=palavra
        elif contextoValido(palavra):
          contex+=palavra
        elif projetoValido(palavra):
          proj+=palavra
      parametros =[data,hora,pri,descricao,contex,proj]
      for parametro in parametros:
        if parametro!='':
          novaAtividade+= parametro +' '
      novaAtividade=novaAtividade.strip()      
          

    else:
      novaAtividade+=descricao
  return novaAtividade
  

# Valida a prioridade.
def prioridadeValida(pri):
  if len(pri)==3 and pri[0]=="(" and pri[2]==")":
    if 'a'<=pri[1]<='z' or 'A'<=pri[1]<='Z':
      return True
  return False


# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
    horas = (horaMin[0] +horaMin[1])
    minutos =(horaMin[2] +horaMin[3])
    if horas<'00' or horas>'23' or minutos <'00' or minutos>'59':
      return False
    else:
      return True
# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data):
    if soDigitos(data) and len(data)==8:
      dia = data[0]+data[1]
      mes = data[2]+data[3]
      #ano = data[4]+data[5]+data[6]+data[7]
      #meses31=['01','03','05','07','08','10','12']
      meses30=['04','06','09','11']
      if '01'<=mes<='12':
        if finder(meses30,mes):
          if "00"<=dia<="30":
            return True
          else:
            return False
                
        elif mes == '02':
          if '00'<=dia<='29':
              return True
          else:
              return False
        else:
          if '00'<=dia<='31':
              return True
          else:
              return False
      else:
        return False
     
def finder(lista,x):
    if len(lista)==1:
        if lista[0]==x:
            return True
        else:
            return False
    elif lista[-1]==x:
        return True
    else:
        lista.pop(-1)
        return finder(lista,x)
        
# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):
  if len(proj)>=2 and proj[0]=='+':
    return True
  return False
  
# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):
  if len(cont)>=2 and cont[0]=='@':
    return True
  return False

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
def organizar(linhas):
    itens = []
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
    for l in linhas:
      if horaValida(l):
          hora+=l
      elif dataValida(l):
          data+=l 
      elif contextoValido(l):
          contexto+=l
      elif projetoValido(l):
          projeto+=l
      elif prioridadeValida(l):
          pri+=l
      else:
          desc+=l+' '  
    desc=desc.strip()
    itens.append((desc, (data, hora, pri, contexto, projeto)))

    return itens

 

    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis. 

    ################ COMPLETAR



# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
def listar():
  linhas = adjListar()[0]
  indices=[linhas[x][1] for x in range(len(linhas))]
  frases=[linhas[x][0] for x in range(len(linhas))]
  cores=[RED,BLUE,CYAN,YELLOW,GREEN]
  frases = [frase.split() for frase in frases]
  frases = [organizar(frase)[0] for frase in frases]
  for i in range(len(frases)):
    if frases[i][1][2]!='':
      if frases[i][1][2].upper()== '(A)':
        frase= manipular(frases[i][0],frases[i][1])
        frase=(printCores(frase,cores[0]))
      elif frases[i][1][2].upper() == '(B)':
        frase= manipular(frases[i][0],frases[i][1])
        frase=(printCores(frase,cores[1]))
      elif frases[i][1][2].upper() == '(C)':
        frase= manipular(frases[i][0],frases[i][1])
        frase=(printCores(frase,cores[3]))
      elif frases[i][1][2].upper() == '(D)':
        frase = manipular(frases[i][0],frases [i][1])
        frase =(printCores(frase,cores[4]))
      else:
        frase= manipular(frases[i][0],frases[i][1])
    else:
      frase =manipular(frases[i][0],frases[i][1])     
    print(indices[i] ,frase)
  ################ COMPLETAR
def adjListar():
  arq = open('todo.txt','r',encoding='utf-8')
  textos = arq.readlines()
  linhas = []
  #linhas eh uma lista de itens
  for i in textos:
    i = i.split()
    linha=organizar(i)
    linhas+=linha
  linhasOrd = ordenarPorPrioridade(ordenarPorDataHora(linhas))
  linhaArq = [[manipular(linhas[x][0],linhas[x][1])] + [x+1] for x in range(len(linhas))]
  linhaBase =[manipular(linhas[x][0],linhas[x][1]) for x in range(len(linhas))]
  #print(linhaBase)
  #print(linhaArq)
  linhaPrint=[[manipular(linhasOrd[x][0],linhasOrd[x][1])]  for x in range(len(linhasOrd))]
  #print(linhaPrint)
  for i in range(len(linhaPrint)):
    for y in range(len(linhaPrint)):
      if linhaPrint[i][0] ==linhaArq[y][0]:
        linhaPrint[i]+=[linhaArq[y][1]]
  return linhaPrint,linhaBase
  
                   
def ordenarPorDataHora(itens):
  itens = ordData(ordenarHora(itens))

  return itens


def ordenarHora(itens):
  sHora =[itens[x] for x in range(len(itens)) if itens[x][1][1]=='']
  cHora =[itens[x] for x in range(len(itens)) if itens[x][1][1]!='']
  i=0
  while i<len(cHora):
    i+=1
    y=0
    while y<len(cHora)-1:
      if cHora[y][1][1]>cHora[y+1][1][1]:
        temp = cHora[y+1]
        cHora[y+1] =cHora[y]
        cHora[y] =temp
        y+=1
      else:
        y+=1
  return cHora +sHora

def ordData(itens):
  semData =[itens[x] for x in range(len(itens)) if itens[x][1][0] =='']
  comData =[itens[x] for x in range(len(itens)) if itens[x][1][0] !='']
  for i in range (len(comData)):
    for y in range(len(comData)-1):
      if inverter(comData[y][1][0])>inverter(comData[y+1][1][0]):
        temp =comData[y+1]
        comData[y+1] =comData[y]
        comData[y]=temp
  return comData+semData

#função usada para inverter a data na hora de comparar o'tamanho/Valor' da data, assim simplificando o processo de comparação
def inverter(data):
    data=list(data)
    data = data[4]+data[5]+data[6]+data[7]+data[2]+data[3]+data[0]+data[1]
    return data


   
def ordenarPorPrioridade(itens):
  semPrioridade = [itens[x] for x in range(len(itens)) if itens[x][1][2]=='']
  prioridade = [itens[x] for x in range(len(itens)) if itens[x][1][2]!='']
  i=0
  if len(prioridade)>1:
    while i<len(prioridade):
      i+=1
      y=0
      while y<len(prioridade)-1:
        if prioridade[y][1][2].upper()>prioridade[y+1][1][2].upper():
          temp = prioridade[y+1]
          prioridade[y+1]=prioridade[y]
          prioridade[y]=temp
          y+=1
        else:
          y+=1

  return prioridade + semPrioridade
    
def fazer(num):
  lista = adjListar()[0]
  indiceFeito=''
  for i in range(len(lista)):
    if lista[i][1]==num:
      indiceFeito=i
  if indiceFeito!='':
    feito=lista[indiceFeito]
    feito=feito[0]
    arq= open('done.txt','a',encoding='utf-8')
    arq.write(feito + '\n')
    arq.close() 
    return remover(num)
  else:
    print(f'ERRO , {num} NÃO ESTÁ PRESENTE NA LISTAGEM')

def remover(x):
  lista = adjListar()[0]
  aux= adjListar()[1]
  remover =''
  for i in range(len(lista)):
    if lista[i][1]==x:
      remover=i
  if remover!='':
    removido = lista.pop(remover)
    removido=removido[0]
    for i in range(len(aux)):
      if aux[i]==removido:
        indRmv=i
    aux.pop(indRmv)
    arq = open('todo.txt','w',encoding='utf-8')
    for i in range(len(aux)):
      arq.write(aux[i] + "\n")
    arq.close()
  else:
    print(f"o número {x} não está listado nas atividades")
  ################ COMPLETAR

# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):
  if type(num)==int and type(prioridade)==str:
    lista=adjListar()[0]
    indice =''
    for i in range(len(lista)):
      if lista[i][1] == num:
        indice = i
    if indice!='':
      remover(num)    
      linha = lista.pop(indice)
      frase = linha[0]
      frase = frase.split()
      frase = organizar(frase)
      #lista de tupla vira uma tupla de dois elementos
      frase = frase[0]
      novaFrase = (frase[0],(frase[1][0],frase[1][1],'('+prioridade+')',frase[1][3],frase[1][4]))
      adicionar(novaFrase[0],novaFrase[1])

    else:
      print(f'Erro, o numero {num} não se encontra na listagem')
  else:
    print('ERRO! COMANDO INVALIDO')

  ################ COMPLETAR

  return

# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos) :
  if comandos[1] == ADICIONAR:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'adicionar'
    #return print(organizar(comandos))
    itemParaAdicionar = organizar((comandos))[0]
    #itemParaAdicionar = organizar([' '.join(comandos)])[0]
    #itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
    #adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
    return adicionar(itemParaAdicionar[0], itemParaAdicionar[1])
  elif comandos[1] == LISTAR:
    comandos.pop(0) 
    comandos.pop(0)
    return listar()
  
  
    ################ COMPLETAR

  elif comandos[1] == REMOVER:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove remover
    try:
      x=int(comandos.pop(0))
      if type(x)==int:
        return remover(x)
    except:
      print("ERRO! COMANDO INVALIDO")
    ################ COMPLETAR    
      
  elif comandos[1] == FAZER:
    comandos.pop(0)
    comandos.pop(0)
    n = comandos.pop(0)
    try:
      return fazer(int(n))
    except:
      print('ERRO! COMANDO INVALIDO')

    ################ COMPLETAR

  elif comandos[1] == PRIORIZAR:
    comandos.pop(0)
    comandos.pop(0)
    n =comandos.pop(0)
    pri=comandos.pop(0)
    try:
      n=int(n)
      pri=str(pri)
      return priorizar(n,pri)
    except:
      print('Comando invalido')

    ################ COMPLETAR

  else :
    print("Comando inválido.")
    
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)
