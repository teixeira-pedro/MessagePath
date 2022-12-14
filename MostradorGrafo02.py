
from random import randint
from pyvis.network import Network
import networkx as nx
#from GrafoPost import *
from GrafoPost02 import *
from copy import deepcopy
PIXMAX=1000
#https://pypi.org/project/pyvis-timeline/
#https://pyvis.readthedocs.io/en/latest/tutorial.html#getting-started
def taest2():
    #FUNCIONA
    nx_graph = nx.cycle_graph(10)
    nx_graph.nodes[1]['title'] = 'Number 1'
    nx_graph.nodes[1]['group'] = 1
    nx_graph.nodes[3]['title'] = 'I belong to a different group!'
    nx_graph.nodes[3]['group'] = 10
    nx_graph.add_node(20, size=20, title='couple', group=2)
    nx_graph.add_node(21, size=15, title='couple', group=2)
    nx_graph.add_edge(20, 21, weight=5)
    nx_graph.add_node(25, size=25, label='lonely', title='lonely node', group=3)
    nt = Network('500px', '500px')
    # populates the nodes and edges data structures
    nt.from_nx(nx_graph)
    nt.show('nx.html')

def grafo_de_teste():
    G=cria_digrafo()
    posts=cria_dict_posts()


    add_no_grafo(G,posts,{"id":3,'conteudo':['post...3..'
        ,'https://sites.google.com/a/ic.uff.br/fernanda/_/rsrc/1489691433727/home/logo-ic-uff.png',
                                             2,criaDataHora(1,10,2022,0,0),'https://www.uff.br','user'+str(randint(0,100000000))]})
    add_no_grafo(G,posts,{"id":4,'conteudo':['post...4..'
        ,'https://sites.google.com/a/ic.uff.br/fernanda/_/rsrc/1489691433727/home/logo-ic-uff.png',
                                             2,criaDataHora(4,10,2022,0,0),'https://www.uff.br','user'+str(randint(0,100000000))]})
    add_no_grafo(G,posts,{"id":6,'conteudo':['post...6..'
        ,'https://sites.google.com/a/ic.uff.br/fernanda/_/rsrc/1489691433727/home/logo-ic-uff.png',
                                             2,criaDataHora(4,10,2022,0,0),'https://www.uff.br','user'+str(randint(0,100000000))]})
    add_no_grafo(G,posts,{"id":7,'conteudo':['post...7..'
        ,'https://sites.google.com/a/ic.uff.br/fernanda/_/rsrc/1489691433727/home/logo-ic-uff.png',
                                             7,criaDataHora(5,10,2022,0,0),'https://www.uff.br','user'+str(randint(0,100000000))]})
    add_no_grafo(G,posts,{"id":8,'conteudo':['post...8..'
        ,'https://sites.google.com/a/ic.uff.br/fernanda/_/rsrc/1489691433727/home/logo-ic-uff.png',
                                             2,criaDataHora(7,10,2022,0,0),'https://www.uff.br','user'+str(randint(0,100000000))]})
    add_no_grafo(G,posts,{"id":9,'conteudo':['post...8..'
        ,'https://sites.google.com/a/ic.uff.br/fernanda/_/rsrc/1489691433727/home/logo-ic-uff.png',
                                             2,criaDataHora(9,10,2022,0,0),'https://www.uff.br','user'+str(randint(0,100000000))]})


    add_aresta_grafo(G,3,4,2)
    add_aresta_grafo(G,3,6,0.5)
    add_aresta_grafo(G,6,7,0.5)
    add_aresta_grafo(G,7,9,0.5)
    add_aresta_grafo(G,7,8,0.5)
    a='''
    for i in range (1,100):
        add_no_grafo(G, posts, {"id": 9+i, 'conteudo': ['post...'+str(9+i)+'..'
            , 'https://sites.google.com/a/ic.uff.br/fernanda/_/rsrc/1489691433727/home/logo-ic-uff.png',
                                                      2, '10/10/2012', 'https://www.uff.br']})
        add_aresta_grafo(G, randint(9,100), randint(9,100), 0.5)'''
    ordem=index_posts_ordenados_tempo(posts)
    #print(ordem)

    G=ordena_posicao_tela_grafo_x(G,ordem,PIXMAX)
    #print(ordem)
    ordemY = i998(converteLisPost(ordem,posts),PIXMAX/2)
    #for i in ordemY:
    #    print(i)
    #ordemY = index_posts_nivel(ordem,posts)  ####  DEBUG
    G = ordena_posicao_tela_grafo_y(G, ordemY, PIXMAX) #TEST
    return G,posts

def taest3():
    from random import randint
    G=cria_digrafo()
    posts=cria_dict_posts()


    add_no_grafo(G,posts,{"id":3,'conteudo':['post...3..'
        ,'https://sites.google.com/a/ic.uff.br/fernanda/_/rsrc/1489691433727/home/logo-ic-uff.png',
                                             2,criaDataHora(1,10,2022,0,0),'https://www.uff.br','user'+str(randint(0,100000000))]})
    add_no_grafo(G,posts,{"id":4,'conteudo':['post...4..'
        ,'https://sites.google.com/a/ic.uff.br/fernanda/_/rsrc/1489691433727/home/logo-ic-uff.png',
                                             2,criaDataHora(4,10,2022,0,0),'https://www.uff.br','user'+str(randint(0,100000000))]})
    add_no_grafo(G,posts,{"id":6,'conteudo':['post...6..'
        ,'https://sites.google.com/a/ic.uff.br/fernanda/_/rsrc/1489691433727/home/logo-ic-uff.png',
                                             2,criaDataHora(4,10,2022,0,0),'https://www.uff.br','user'+str(randint(0,100000000))]})
    add_no_grafo(G,posts,{"id":7,'conteudo':['post...7..'
        ,'https://sites.google.com/a/ic.uff.br/fernanda/_/rsrc/1489691433727/home/logo-ic-uff.png',
                                             7,criaDataHora(5,10,2022,0,0),'https://www.uff.br','user'+str(randint(0,100000000))]})
    add_no_grafo(G,posts,{"id":8,'conteudo':['post...8..'
        ,'https://sites.google.com/a/ic.uff.br/fernanda/_/rsrc/1489691433727/home/logo-ic-uff.png',
                                             2,criaDataHora(7,10,2022,0,0),'https://www.uff.br','user'+str(randint(0,100000000))]})
    add_no_grafo(G,posts,{"id":9,'conteudo':['post...8..'
        ,'https://sites.google.com/a/ic.uff.br/fernanda/_/rsrc/1489691433727/home/logo-ic-uff.png',
                                             2,criaDataHora(9,10,2022,0,0),'https://www.uff.br','user'+str(randint(0,100000000))]})


    add_aresta_grafo(G,3,4,2)
    add_aresta_grafo(G,3,6,0.5)
    add_aresta_grafo(G,6,7,0.5)
    add_aresta_grafo(G,7,9,0.5)
    add_aresta_grafo(G,7,8,0.5)
    a='''
    for i in range (1,100):
        add_no_grafo(G, posts, {"id": 9+i, 'conteudo': ['post...'+str(9+i)+'..'
            , 'https://sites.google.com/a/ic.uff.br/fernanda/_/rsrc/1489691433727/home/logo-ic-uff.png',
                                                      2, '10/10/2012', 'https://www.uff.br']})
        add_aresta_grafo(G, randint(9,100), randint(9,100), 0.5)'''
    ordem=index_posts_ordenados_tempo(posts)
    #print(ordem)

    G=ordena_posicao_tela_grafo_x(G,ordem,PIXMAX)
    #print(ordem)
    ordemY = i998(converteLisPost(ordem,posts),PIXMAX/2)
    #for i in ordemY:
    #    print(i)
    #ordemY = index_posts_nivel(ordem,posts)  ####  DEBUG
    G = ordena_posicao_tela_grafo_y(G, ordemY, PIXMAX) #TEST

    nt = Network('800px', str(PIXMAX)+'px',directed =True)
    # populates the nodes and edges data structures
    nt.from_nx(G)
    nt.toggle_physics(False)
    nt.show('nx3.html')
    print(posts)


def achaTweetNoGrafo(Gs,noh):
    for i in range(len(Gs)):
        if noh in Gs[i].nodes:
            return i
    return -1

def Grafo2Mostrador(G,posts,nome_html,PXMAX,pixelsMostrador):
    if pixelsMostrador <800:
        pixelsMostrador=800
    if pixelsMostrador>PXMAX:
        PXMAX=pixelsMostrador+200
    ordem=index_posts_ordenados_tempo(posts)
    G=ordena_posicao_tela_grafo_x(G,ordem,PXMAX)
    #print(ordem)
    ordemY = i998(converteLisPost(ordem,posts),PXMAX/2)
    #for i in ordemY:
    #    print(i)
    #ordemY = index_posts_nivel(ordem,posts)  ####  DEBUG
    G = ordena_posicao_tela_grafo_y(G, ordemY, PXMAX) #TEST

    G= reordenaSozinhos(G,ordemY)

    nt = Network(str(pixelsMostrador)+'px', str(PIXMAX)+'px',directed =True)
    # populates the nodes and edges data structures
    nt.from_nx(G)
    nt.toggle_physics(False)
    nt.show(nome_html+'.html')

#taest2()
#taest3()
