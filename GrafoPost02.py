# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from copy import deepcopy
import networkx as _NX_
import pylab
import pandas as _PAN_
import numpy as _NPY_
import matplotlib.pyplot as _PLOTTER_
from datetime import datetime
import datetime as DTT
from Util import *
from random import randint

def cria_grafo():
    return _NX_.Graph()

def cria_digrafo():
    return _NX_.DiGraph()

def cria_digrafo_comId(id):
    return _NX_.DiGraph(idGrafo=id)

def cria_dict_posts():
    return {}

def marca_aresta(G,Vi,Vj,marca):
    _NX_.set_edge_attributes(G,{(Vi,Vj):{"cost":marca}})


def graphs_equal(graph1, graph2):
    """Check if graphs are equal.

    Equality here means equal as Python objects (not isomorphism).
    Node, edge and graph data must match.

    Parameters
    ----------
    graph1, graph2 : graph

    Returns
    -------
    bool
        True if graphs are equal, False otherwise.
    """
    return (
        graph1.adj == graph2.adj
        and graph1.nodes == graph2.nodes
        and graph1.graph == graph2.graph
    )


def instante_tempo(index_no,posts):
    '''TESTAR'''
    '''em desenvolvimento'''
    #from random import randint
    try:
        return str2Datetime(posts[index_no][3])
    except:
        return None

def converteLisPost(l,posts):
    resp=[]
    for i in l:
        resp.append((i,instante_tempo(i,posts)))
    return resp
#def converteLisMock(l,posts):
#    resp=[]
#    k=[3, 6, 6, 7, 8, 9]
#    for i in range(len(l)):
#        resp.append((l[i],k[i]*100))
#    return resp
def i998(L,PIXMAX):
    #for i in L:
    #    print(i)
    resp=[]
    i=0
    while i< len(L)-1 :
        buffer=[]
        index = L[i][0]
        VAL = L[i][1]
        #index_prox = L[i+1][0]  #POSSIVEL BUG AQUI
        VAL_prox = L[i+1][1]
        buffer.append([index,VAL])
        while i<len(L)-1 and VAL_prox==VAL :
            i=i+1
            index = L[i][0]
            VAL = L[i][1]
            #index_prox = L[i + 1][0] #POSSIVEL BUG AQUI


            try:
                VAL_prox = L[i + 1][1]
            except:
                VAL_prox = L[i][1]
            #VAL_prox = L[i + 1][1]

            buffer.append([index,VAL])
        i=i+1
        resp.append({'steps':int(PIXMAX/len(buffer)),'buffer':buffer})

    return resp

def index_posts_nivel(l,posts):
    resp=[]
    while l!=[]:
        pil=[]
        pil=push(pil,pop(l))
        print('antes :',instante_tempo(top(pil),posts) ,'///depois :', instante_tempo(top(l),posts),
              instante_tempo(top(pil),posts) == instante_tempo(top(l),posts),
              type(instante_tempo(top(pil),posts)))
        a=instante_tempo(top(pil),posts)
        b=instante_tempo(top(l),posts)
        #while instante_tempo(top(pil),posts) == instante_tempo(top(l),posts) and l!=[] :
        while a == b and l!=[] :
        #while top(pil) == top(l) and l!=[] :
                 pil=push(pil,pop(l))
                 a=instante_tempo(top(pil),posts)
                 b=instante_tempo(top(l),posts)
        resp.append(pil)
    resp2=[]
    for i in resp:
        resp2=[i]+resp2
    return resp

def ordena_posicao_tela_grafo_x(G,ordem,pxmax):
    if not ordem :
        return G
    step=pxmax/len(ordem)
    #print(ordem)
    #print(G.nodes)
    for i in range(len(ordem)):
        #print(i)
        #print(G[ordem])
        #print(G.nodes[ordem[i]])
        #print(G)
        if ordem[i] in G.nodes:
            G.nodes[ordem[i]]['x']=i*step
            G.nodes[ordem[i]]['y']=10
        #3q49w7oejyrfgvuwaq73gofe8yh\njsk
    return G

def incre(i):
    PSI=randint(100,500)
    if i%2 ==0:
        return -PSI/randint(1200,2500)
    else:
        return PSI/randint(1200,2500)


def ordena_posicao_tela_grafo_y_discard(G, ordem, pxmax):
    '''TESTAR'''
    if not ordem:
        return G
    # print(ordem)
    # LSL=len_sublistas(ordem)
    # mxLSL=max(LSL)

    j = 0

    for nivel in ordem:
        step = nivel['steps']
        nos_nivel = nivel['buffer']

        if len(nos_nivel) == 1 and j != 0:
            G.nodes[nos_nivel[0][0]]['y'] = step * (1 + incre(j))
        else:
            for i in range(len(nos_nivel)):
                # print(i)
                # print(G[ordem])
                # G.nodes[ordem[i]]['x']=i*step
                # print(nos_nivel[i])
                G.nodes[nos_nivel[i][0]]['y'] = (i + 1) * step

        j = j + 1

    step = pxmax / len(ordem)
    i = 0
    for nivel in ordem:
        for no in nivel['buffer']:
            G.nodes[no[0]]['x'] = i * step
        i = i + 1
        # 3q49w7oejyrfgvuwaq73gofe8yh\njsk
    return G

def reordenaSozinhos(G,ordem):
    for i in range(len(ordem)):
        nivel=ordem[i]
        if i!=0:
            if len(nivel['buffer']) ==1 :
                no_indice=nivel['buffer'][0][0]
                if no_indice in G.nodes:
                    G.nodes[no_indice]['y']=G.nodes[no_indice]['y']*(1+incre(i))
                #print('mexer nivel (', i, '):', nivel, 'com pixels=', G.nodes[no_indice]['y'])
    return G

def ehNoEspecial(no):
    return no <= 0

def ordena_posicao_tela_grafo_y(G,ordem,pxmax):
    '''TESTAR'''
    if not ordem :
        return G
    #print(ordem)
    #LSL=len_sublistas(ordem)
    #mxLSL=max(LSL)
    for nivel in ordem:
        step=nivel['steps']
        nos_nivel=nivel['buffer']
        for i in range(len(nos_nivel)):
        #print(i)
        #print(G[ordem])
        #G.nodes[ordem[i]]['x']=i*step
            #print(nos_nivel[i])
            if nos_nivel[i][0] in G.nodes:
                G.nodes[nos_nivel[i][0]]['y']=(i+1)*step
    step = pxmax / len(ordem)
    i=0
    for nivel in ordem:
        for no in nivel['buffer']:
            if no[0] in G.nodes:
                G.nodes[no[0]]['x']=i*step
        i=i+1
        #3q49w7oejyrfgvuwaq73gofe8yh\njsk
    return G

def add_no_especial(G1,G2,idSimilA,idSimilB,DICT):
    #TEMPO TEM DE SER REGISTRADO NO NOVO NÓ
    novo_id=-(idSimilA+idSimilB)
    post1 = DICT[idSimilA]#update(post)
    post2 = DICT[idSimilB]#update(post)
    try:
        DICT[-idSimilB] = post2["conteudo"]  # update(post)
    except Exception as e:
        print(e)
    try:
        DICT[-idSimilA] = post2["conteudo"]  # update(post)
    except Exception as e:
        print(e)
    if not -idSimilB in G1.nodes:
        print(post2)
        G1.add_node(-idSimilB,label='<a href="'+str(6)+'.html'+'" >Claim : [claim] '+
                                  str(idSimilB)+'\n' + datetime2str(post2[3])+'</a>',
                    title=converte_conteudo(post2),
                    group=post2[2],
                    shape='square',
                    id_original=idSimilB
                    )
    if not -idSimilA in G2.nodes:
        G2.add_node(-idSimilA,label='<a href="'+str(6)+'.html'+'" >Claim : [claim] '+
                                  str(idSimilA)+'\n' + datetime2str(post1[3])+'</a>',
                    title=converte_conteudo(post1),
                    group=post1[2],
                    id_original=idSimilA
                    )
    return -idSimilA,-idSimilB


def add_no_grafo(G,DICT,*posts):

    if G==None or DICT==None:
        print('erro ao adicionar no grafo')
        return -1

    posts_adicionados=0
    for post in posts:
            DICT[post["id"]]=post["conteudo"]#update(post)
            #G.add_nodes_from([post["id"]])
            G.add_node(post["id"],
                       title=converte_conteudo(post['conteudo']),
                       label=str(post["id"])+'\n'+datetime2str(post['conteudo'][3]) ,
                       group=post['conteudo'][2]
                       #node_shape = 's'
                       #x=Xpos,
                       #y=10
                       #image='post[1]'
                       )
            print('&&&&& Nó guardado : ',post["id"],converte_conteudo(post['conteudo']),str(post["id"])+'\n'+datetime2str(post['conteudo'][3]) ,post['conteudo'][2])
    return 1

def converte_conteudo(post):
    #print(post,'*****',post==[], post==None , len(post)<6)
    '''['post...3..', 'imagem.jpg', 2, '10/10/2012']'''
    if post==[] or post==None or len(post)<6:
        return ''
    post[3]=datetime2str(post[3])
    post[4]=str(post[4])
    post[1]=str(post[1])
    if not AND(TIPOIGUAL('',post[0]),TIPOIGUAL(post[1],post[0]),
               TIPOIGUAL(post[1],post[3]),TIPOIGUAL(post[1],post[4]),TIPOIGUAL(post[1],post[4])):
        return ''
    #print('✉[CONTEUDO]:'+post[0]+'<br>⏰[DATAHORA]:'+post[3]+'<br><table>📷[ANEXO]:'+'<img src="'+post[1]+'"  height="70"></table><br>'+'<a href="'+post[4]+'" target="_blank">🌎[LINK]</a><br>👤[USUARIO]:'+post[5])
    return '✉[CONTEUDO]:'+post[0]+'<br>⏰[DATAHORA]:'+post[3]+'<br><table>📷[ANEXO]:'+'<img src="'+post[1]+'"  height="70"></table><br>'+'<a href="'+post[4]+'" target="_blank">🌎[LINK]</a><br>👤[USUARIO]:'+post[5]#+'<br>'+('-'*20)+'<blockquote class="twitter-tweet"><p lang="pt" dir="ltr"><a href="https://twitter.com/hashtag/OportunidadesUFF?src=hash&amp;ref_src=twsrc%5Etfw">#OportunidadesUFF</a>/ Faça parte do Fulbright Amazônia: uma iniciativa que reúne membros de vários países com o intuito de formular ações em prol do meio ambiente. Serão oferecidas 4 bolsas para brasileiros participarem do programa.<br><br>Mais informações 🔗<a href="https://t.co/5nFfRrvLKY">https://t.co/5nFfRrvLKY</a> <a href="https://t.co/bgY1ZUMyh0">pic.twitter.com/bgY1ZUMyh0</a></p>&mdash; UFF (@uff_br) <a href="https://twitter.com/uff_br/status/1588622108837482497?ref_src=twsrc%5Etfw">November 4, 2022</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'

def remove_aresta_grafo(G,Vi,Vj):
     G.remove_edge(Vi,Vj)

def remove_no_grafo(G,post,DICT):
    G.remove_node(post)
    DICT.pop(post)

def add_aresta_grafo(G,Vi,Vj,custo):
    if custo==None:
        custo=0
    G.add_edge(Vi,Vj,weight=custo)
    #marca_aresta(G,Vi,Vj,custo)

def desenha_grafo(G):
    pylab.figure(1)
    pos=_NX_.spring_layout(G)
    #_NX_.draw(G,with_labels=True)
    _NX_.draw(G,pos,with_labels=True)
    #_NX_.draw_networkx_edge_labels(G,pos,_NX_.get_edge_attributes(G,"cost"))
    _NX_.draw_networkx_edge_labels(G,pos)
    _PLOTTER_.show()

def index_posts_ordenados_tempo(posts):
    '''retorna ordenado por data os indices dos tweets no dicionario'''
    postsCOPY=deepcopy(posts)
    #print(posts)
    #print(postsCOPY)
    SORTED=sorted(postsCOPY.items(),key= lambda x:x[1][3])
    #print('sorted',SORTED)
    resp=[]
    for item in SORTED:
        chave=item[0]
        resp.append(chave)
    return resp

# Press the green button in the gutter to run the script.
def taeste():
    G=cria_grafo()
    posts=cria_dict_posts()

    add_no_grafo(G,posts,{"id":3,'conteudo':['post...3..','https://pt.wikipedia.org/wiki/Ficheiro:UFF_bras%C3%A3o.png',
                                             2,'10/10/2012','https://www.uff.br']})
    add_no_grafo(G,posts,{"id":4,'conteudo':['post...4..','https://pt.wikipedia.org/wiki/Ficheiro:UFF_bras%C3%A3o.png',
                                             2,'10/10/2012','https://www.uff.br']})
    add_no_grafo(G,posts,{"id":5,'conteudo':['post...5..','https://pt.wikipedia.org/wiki/Ficheiro:UFF_bras%C3%A3o.png',
                                             2,'10/10/2012','https://www.uff.br']})
    add_no_grafo(G,posts,{"id":6,'conteudo':['post...6..','https://pt.wikipedia.org/wiki/Ficheiro:UFF_bras%C3%A3o.png',
                                             2,'10/10/2012','https://www.uff.br']})
    add_no_grafo(G,posts,{"id":7,'conteudo':['post...7..','https://pt.wikipedia.org/wiki/Ficheiro:UFF_bras%C3%A3o.png',
                                             2,'10/10/2012','https://www.uff.br']})
    add_no_grafo(G,posts,{"id":8,'conteudo':['post...8..','https://pt.wikipedia.org/wiki/Ficheiro:UFF_bras%C3%A3o.png',
                                             2,'10/10/2012','https://www.uff.br']})
    add_no_grafo(G,posts,{"id":9,'conteudo':['post...9..','https://pt.wikipedia.org/wiki/Ficheiro:UFF_bras%C3%A3o.png',
                                             2,'10/10/2012','https://www.uff.br']})

    add_aresta_grafo(G,3,4,3)
    add_aresta_grafo(G,4,6,0.75)
    add_aresta_grafo(G,6,7,0.75)
    add_aresta_grafo(G,7,9,0.75)
    add_aresta_grafo(G,7,8,0.75)

    print(posts)
    print(G.nodes,G.edges)

    desenha_grafo(G)
    #pylab.figure(1)
    #pos=_NX_.spring_layout(G)
    #_NX_.draw(G,with_labels=True)
    #_NX_.draw(G,pos)
    #_NX_.draw_networkx_edge_labels(G,pos,_NX_.get_edge_attributes(G,"cost"))
    #_NX_.draw_networkx_edge_labels(G,pos)

    remove_no_grafo(G,3,posts)
    print(posts)
    print(G.nodes,G.edges)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
#taeste()