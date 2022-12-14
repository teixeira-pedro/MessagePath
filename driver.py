from APITwitter import *
from MostradorGrafo02 import *
from random import randint
from time import sleep
from nlp import *
from finalizaFrontEnd import *

MAX_TW = 5
MAX_LEVEL = 5

######################MÉTODOS DEPRECIADOS#############################
def montaGrafoClaimTwitter_old(claim_query,MAX,API,DAT):
    '''DEPRECIADO'''
    if MAX_TW < MAX and MAX <=0 :
        MAX=MAX_TW
    LL = API.search_tweets(q=claim_query,count=MAX,include_entities=True)
    ##LL=FP_OBJ_OPEN('LL.TWDAT')
    #print(LL)
    Γ=[]
    for L in LL:
        Γ.append(tweeet2No(Tuite(L)))
    G=cria_digrafo()
    for g in Γ:
        #print(g)
        γ=g[0][1]
        #print(γ)
        add_no_grafo(G,DAT,γ)
    for L in LL:
        g=tweeet2No(Tuite(L))
        γ=g[0]
        #print(g,L)
        print('RESPOSTAS E REPLIES DE ', γ[1]['id'],Tuite(L)['id'])

        print(γ[1]['id'],Tuite(L)['id'])
        #getRetweetsEReplies
        ẞ = getRetweetsEReplies(γ[1]['id'],API,MAX)
        for reposRet in ẞ:
            print( 'reposRet:',reposRet)
        #input('AGUARDANDO...')
        #ẞ = getReplies(γ[1]['id'],γ)+getRetweets(Tuite(L)['id'],API,MAX)
        #print(ẞ)
        print('indo pra recursão')
        montaGrafoRecursivo_OLD(γ,ẞ,DAT,G,API,MAX,0)
        print('********FIM********RESPOSTAS E REPLIES DE ', γ[1]['id'], Tuite(L)['id'])
    #FP_OBJ_SAVE(G,'G_Twitter'+datetime2str(datetime.now()).replace(':',"_").replace(" ",'_')+'.GRDAT')
    return G
def montaGrafoRecursivo_OLD(γ,ẞ,DAT,G,API,MAX,level):
    '''DEPRECIADO'''
    #level=level+1
    if level >= MAX_LEVEL :
        print('level Maximo')
        return
    print(level)
    for i in ẞ:
        print(i)
    print('-'*80)
    Ꜩ=ẞ
    #TZETT = tweeet2No(ESZETT)
    for tt in Ꜩ:
        ꜩ=tt[0][1]
        add_no_grafo(G,DAT,ꜩ)
        γ_=None
        ꜩ2 = None
        try:
            γ_=γ[0]
        except:
            print('γ:',γ)
            γ_=γ['id']

        try:
            ꜩ2=ꜩ['id']
        except:
            print('ꜩ:',ꜩ)
            ꜩ2=ꜩ[0]
        print('ꜩ2:',ꜩ2,'''
        y_''',γ_,'''
        y''',γ)
        add_aresta_grafo(G=G,Vi=γ_,Vj=ꜩ2,custo=3)
    for tt in Ꜩ:
        ꜩ=tt[0][1]
        try:
            ẞ_i = getRetweetsEReplies(ꜩ['id'], API, MAX)
        except:
            ẞ_i = getRetweetsEReplies(ꜩ, API, MAX)
        #ẞ_i = getReplies(ꜩ['id'],ꜩ)+getRetweets(ꜩ['id'],API,MAX)
        t=randint(2000,8888)/1000
        print('aguardando tempo para não floodar API...','aguarde por [',t,'] segundos')
        sleep(t)
        print('ꜩ em recursão (',level,') :',ꜩ,ẞ_i)
        try:
            montaGrafoRecursivo(ꜩ['id'],ẞ_i,DAT,G,API,MAX,level+1)
        except:
            montaGrafoRecursivo(ꜩ,ẞ_i,DAT,G,API,MAX,level+1)
def atualizaGrafo_Similaridade(G,DAT,MODELO_NLP,τ):
    #AJEITAR CHAMADA DOS VETORIZADORES NO MODULO NLP
    #TESTAR
    '''DEPRECIADO'''
    assert type(G)==type(cria_digrafo())
    G_ = deepcopy(G)
    if τ < 0 or τ > 1 :
        return G
    for i in G.nodes :
        for j in G.nodes :
            #print('i:',i,'\n','j:',j,'\n','i->j:',(i,j),'\n','GG.EE:',G.edges)
            #print('Ancestrais(i):',nx.ancestors(G,i),'\n','Ancestrais(j):',nx.ancestors(G,j),
            #      '\n','(i):', G.nodes[i], '\n','(j):', G.nodes[j], '\n')
            #print('data_i:',str2Datetime(DAT[i][3]))
            #print('data_j:',str2Datetime(DAT[j][3]))
            if AND(i!=j,(i,j) not in G.edges, (j,i) not in G.edges,
                    i not in nx.ancestors(G,j), j not in nx.ancestors(G,i),
                    str2Datetime(DAT[i][3])<str2Datetime(DAT[j][3])
                    ):
                #print()
                result=MODELO_NLP(DAT[i][0],DAT[j][0])
                if type(result)==type(.0):
                    theta = result
                else:
                    Ψ=result[0]
                    Φ=result[0]
                    θ=Cos_vet(Ψ,Φ)
                    print('cos θ = cos(<Ψ,Φ) =',θ,'>=',τ,'=τ')

                if θ >= τ:
                    add_aresta_grafo(G_,i,j,θ/2)
    FP_OBJ_SAVE(G_,'G_Simil_Twitter'+datetime2str(datetime.now()).replace(':',"_").replace(" ",'_')+'.GRDAT')
    print('fim analise similaridade')
    return G_
def atualizaGrafo_Similaridade_InterClaim(Gs,TEMPDAT,MODELO_NLP,τ):
    '''DEPRECIADO'''
    DAT=deepcopy(TEMPDAT)
    pilG=[]
    for G in Gs:
        pilG.append(deepcopy(G))
    resp=[]
    while pilG != []:
        G= pop(pilG)
        for G2 in pilG:
            LG=list(G.nodes)
            print(LG)
            for i in LG:
                LG2 = list(G2.nodes)
                print(LG2)
                for i2 in LG2:
                    # print('i:',i,'\n','j:',j,'\n','i->j:',(i,j),'\n','GG.EE:',G.edges)
                    # print('Ancestrais(i):',nx.ancestors(G,i),'\n','Ancestrais(j):',nx.ancestors(G,j),
                    #      '\n','(i):', G.nodes[i], '\n','(j):', G.nodes[j], '\n')
                    # print('data_i:',str2Datetime(DAT[i][3]))
                    # print('data_j:',str2Datetime(DAT[j][3]))
                    if not ehNoEspecial(i) and not ehNoEspecial(i2):
                        print(str2Datetime(DAT[i][3]) ,'<?', str2Datetime(DAT[i2][3]) , ehNoEspecial(i) , ehNoEspecial(i2))
                    else:
                        print(i,i2)

                    if not ehNoEspecial(i) and  not ehNoEspecial(i2) and str2Datetime(DAT[i][3]) < str2Datetime(DAT[i2][3]) :
                        # print()
                        result = MODELO_NLP(DAT[i][0], DAT[i2][0])
                        if type(result) == type(.0):
                            theta = result
                        else:
                            Ψ = result[0]
                            Φ = result[0]
                            θ = Cos_vet(Ψ, Φ)
                            print('cos θ = cos(<Ψ,Φ) =', θ, '>=', τ, '=τ')

                        if θ >= τ:
                            print('criar nos especiais  i->i2 e i2<-i , i->i2 com um lnk na descricao apontando pra G2')
                            print(', i2<-i com um lnk na descricao apontando pra G')
                            print('adicionar i->i2 em G.V e i2<-i em G2.V')
                            novo_id=add_no_especial(G,G2,i,i2,DAT)
                            # Pensar em como o link pro grafo será processado
                            print('criar aresta de i para i->i2 em G.A')
                            print('criar aresta de i2<-i para i2 em G2.A ')
                            add_aresta_grafo(G,i,novo_id[1],θ)
                            add_aresta_grafo(G2,novo_id[0],i2,θ)
        resp.append(G)
    FP_OBJ_SAVE(resp,'Gs_Simil_Twitter_InterClaim'+datetime2str(datetime.now()).replace(':',"_").replace(" ",'_')+'.GRDAT')
    print('fim analise similaridade inter-claim')
    return resp,DAT
def montaGrafoIdTwitter(id,MAX,API,DAT):
    '''DEPRECIADO use como teste 266031293945503744'''
    if MAX_TW < MAX and MAX <=0 :
        MAX=MAX_TW
    LL = Tuite(API.get_status(id=id,include_entities=True))
    Γ = tweeet2No(LL)
    G=cria_digrafo()
    for g in Γ:
        γ=g[1]
        #print(gamma)
        add_no_grafo(G,DAT,γ)
    for g in Γ:
        γ = g[1]
        #print(gamma)
        ẞ = getRetweetsEReplies(γ['id'], API, MAX)
        #ẞ = getReplies(γ['id'],γ)+getRetweets(γ['id'],API,MAX)
        montaGrafoRecursivo_OLD(γ,ẞ,DAT,G,API,MAX,0)
    FP_OBJ_SAVE(G,'G_Twitter'+datetime2str(datetime.now()).replace(':',"_").replace(" ",'_')+'.GRDAT')
    return G
######################MÉTODOS DEPRECIADOS#############################
################################TESTES ANTIGOS############################
def taest2():
    API=TWITTER(CHAVE())
    POSTS=cria_dict_posts()

    ##G=montaGrafoIdTwitter(266031293945503744,5,API,POSTS)
    ##FP_OBJ_SAVE(POSTS,os.path.join('data','posts.last'))
    POSTS=FP_OBJ_OPEN(os.path.join('data','posts.last'))
    G=FP_OBJ_OPEN('G_Twitter2022-11-15_17_45_19.GRDAT')
    #b#G=FP_OBJ_OPEN(os.path.join('data','G_Twitter2022-11-14_23_36_02.GRDAT'))
    #G2,POSTS2=grafo_de_teste()
    Grafo2Mostrador(G,POSTS,'teste2',1000,800)
    G_=atualizaGrafo_Similaridade(G,POSTS,VectorizaSpaCy,0.)
    Grafo2Mostrador(G_,POSTS,'teste2_',1000,800)
def taest3():
    API = TWITTER(CHAVE())
    POSTS = FP_OBJ_OPEN('posts.last2') #cria_dict_posts()
    G=FP_OBJ_OPEN('G_.GRDAT')
    G3=FP_OBJ_OPEN('G3.GRDAT')
    #G=montaGrafoIdTwitter(266031293945503744,5,API,POSTS)
    #G3=montaGrafoClaimTwitter('chloroquine',5,API,POSTS)
    #FP_OBJ_SAVE(POSTS,'posts.last2')
    #FP_OBJ_SAVE(G3,'G3.GRDAT')
    #FP_OBJ_SAVE(G,'G_.GRDAT')
    #POSTS = FP_OBJ_OPEN(os.path.join('data', 'posts.last2'))
    #POSTS = FP_OBJ_OPEN('posts.last2')
    #G = FP_OBJ_OPEN('G_Twitter2022-11-15_17_45_19.GRDAT')
    #G3=FP_OBJ_OPEN('G3.GRDAT')
    ##FP_OBJ_SAVE(POSTS,'POSTS.LAST2')
    ##FP_OBJ_SAVE(G3,'G3.GRDAT')
    Grafo2Mostrador(G3,POSTS,'teste4_',1000,800)
    Grafo2Mostrador(G,POSTS,'teste5_',1000,800)
    #G_=atualizaGrafo_Similaridade_InterClaim([G3,G],POSTS,VectorizaTFID,0.)
    #Grafo2Mostrador(G_[0][1],G_[1],'teste6_',1000,800)
    Gs_=MontaGrafosSimilaridade([G,G3],POSTS,VectorizaTFID,0.0)
    i=0
    for G_ in Gs_ :
        print(G_)
        Grafo2Mostrador(G_,POSTS,'teste_'+str(i)+'_',1000,800)
        i=i+1
    GORIG=[G,G3]
    for i in range(len(Gs_)):
        print(Gs_[i].nodes)
        print(GORIG[i].nodes)
def taest131313(G,POSTS):
    for i in G.nodes:
        print(i)
        print('ancestrais de (', i, '):', nx.ancestors(G, i))
    print((266031293945503744, 1591976519618170887), (266031293945503744, 1591976519618170887) in G.edges)
    for ij in G.edges:
        print(ij)

    print('*' * 80)
    for i in G.nodes:
        for j in G.nodes:
            print('i:', i, '\n', 'j:', j, '\n', 'i->j:', (i, j), '\n', 'GG.EE:', G.edges)
            print('Ancestrais(i):', nx.ancestors(G, i), '\n', 'Ancestrais(j):', nx.ancestors(G, j),
                  '\n', '(i):', G.nodes[i], '\n', '(j):', G.nodes[j], '\n')
            print('DAT[', i, ']:', str2Datetime(POSTS[i][3]))
            print('DAT[', j, ']:', str2Datetime(POSTS[j][3]))
            # print(datetime.now())
def taest5555():
    API=TWITTER(CHAVE())
    POSTS=cria_dict_posts()
    G_cloroqina=montaGrafoClaimTwitter('tratamento precoce salva',50,API,POSTS)
    FP_OBJ_SAVE(G_cloroqina,'G_twitterCloroq.dat')
    FP_OBJ_SAVE(POSTS,'dict_testesTCC.dat')
    #incl :https://twitter.com/ClaudeLuca_/status/1452994179794100233

    G_vacina_miocardite=montaGrafoClaimTwitter('vacina miocardite',50,API,POSTS)
    FP_OBJ_SAVE(G_vacina_miocardite,'G_twitterVacina.dat')
    FP_OBJ_SAVE(POSTS,'dict_testesTCC.dat')
    #incl : https://twitter.com/FernandoVetBio/status/1596295439674150912

    G_covid=montaGrafoClaimTwitter('farsa covid',50,API,POSTS)
    FP_OBJ_SAVE(G_covid,'G_twitterCovid.dat')
    FP_OBJ_SAVE(POSTS,'dict_testesTCC.dat')

    G_vacina_Salva = montaGrafoClaimTwitter('vacina salva', 50, API, POSTS)
    FP_OBJ_SAVE(G_vacina_Salva, 'G_twitterVacinaSalva.dat')
    FP_OBJ_SAVE(POSTS,'dict_testesTCC.dat')

    G_vacina_Sim = montaGrafoClaimTwitter('vacina sim', 50, API, POSTS)
    FP_OBJ_SAVE(G_vacina_Sim, 'G_twitterVacinaSim.dat')
    FP_OBJ_SAVE(POSTS,'dict_testesTCC.dat')

    G_fraude = montaGrafoClaimTwitter('fraude urna', 50, API, POSTS)
    FP_OBJ_SAVE(G_fraude, 'G_fraude.dat')
    FP_OBJ_SAVE(POSTS,'dict_testesTCC.dat')
################################TESTES ANTIGOS############################


def montaGrafoId(id,MAX,API,DAT):
    '''Obtem Grafo de Fluxo de Posts a partir de um post de id específico, ex.: 1595036532179890177'''
    if MAX_TW < MAX and MAX <=0 :
        MAX=MAX_TW
    LL = Tuite(API.get_status(id=id,include_entities=True))
    Γ = tweeet2No(LL)
    G=cria_digrafo()
    for g in Γ:
        γ=g[1]
        #print(gamma)
        add_no_grafo(G,DAT,γ)
        #print(γ, g)
        print('[PROCESSANDO RAIZ ', id, 'raiz =',g[1],'],')
        filhos = getRetweetsEReplies(id,API,MAX)
        for f in filhos:
            ẞ = f[0] #filhos
            #id  #pai raiz
            print( '[ PROCESSANDO TWEET ', id, ' ] adicionando nó ', ẞ[0], ẞ[1])
            add_no_grafo(G, DAT, ẞ[1])
            print('\t[PROCESSANDO TWEET',id,']adicionando aresta (',id,'→',ẞ[0],',)',ẞ[1])
            add_aresta_grafo(G,id,ẞ[0],3)
            montaGrafoRecursivo(ẞ[0],G,DAT,API,MAX,0)
    return G

def montaGrafoClaimTwitter(claim_query,MAX,API,DAT,G_existente):
    '''obtem fluxo de posts a partir dos posts que satisfazem uma determinada busca textual (claim)'''
    if MAX_TW < MAX and MAX <=0 :
        MAX=MAX_TW
    LL = API.search_tweets(q=claim_query,count=MAX,include_entities=True)
    ##LL=FP_OBJ_OPEN('LL.TWDAT')
    #print(LL)
    print('[PROCESSANDO RAIZ ',claim_query,']')
    Γ=[]
    for L in LL:
        Γ.append(tweeet2No(Tuite(L)))
    if G_existente != None:
        G=G_existente
    else:
        G=cria_digrafo()
    for g in Γ:
        #('γ-->',g)
        γ=g[0]
        #print(γ)
        add_no_grafo(G,DAT,γ[1])
        print('[PROCESSANDO RAIZ ', claim_query, 'raiz =',γ[0],γ[1],'],')
    for g in Γ:
        filhos = getRetweetsEReplies(g[0][0],API,MAX)
        for f in filhos:
            ẞ = f[0] #filhos
            γ = g[0] #pai raiz
            print( '[ PROCESSANDO TWEET ', γ[0], ' ] adicionando nó ', ẞ[0], ẞ[1])
            add_no_grafo(G, DAT, ẞ[1])
            print('\t[PROCESSANDO TWEET',γ[0],']adicionando aresta (',γ[0],'→',ẞ[0],',)',ẞ[1])
            add_aresta_grafo(G,γ[0],ẞ[0],3)
            montaGrafoRecursivo(ẞ[0],G,DAT,API,MAX,0)

def montaGrafoRecursivo(γ,G,DAT,API,MAX,level):
    '''função auxiliar de montaGrafoId e montaGrafoClaimTwitter, busca recursivamente por reposts de um determinado post'''
    #level=level+1
    if level >= MAX_LEVEL :
        print('\t'*(level+1),'[rec PROCESSANDO TWEET',γ,' ] level Maximo = ',level)
        return
    print('\t'*(level+1),'[rec PROCESSANDO TWEET ',γ,' ] level = ', level)
    filhos = getRetweetsEReplies(γ,API,MAX)
    print('\t'*(level+1),'[rec PROCESSANDO TWEET ',γ,' ] filhos = ', filhos)
    for f in filhos:
        ẞ = f[0]  # filhos
        print('\t'*(level+1),'[rec PROCESSANDO TWEET ', γ, ' ] adicionando nó ', ẞ[0],ẞ[1])
        add_no_grafo(G,DAT,ẞ[1])
        print('\t'*(level+1),'[rec PROCESSANDO TWEET', γ, ']adicionando aresta (', γ, '→', ẞ[0], ')')
        add_aresta_grafo(G,γ,ẞ[0],3)
    for f in filhos:
        ẞ = f[0]  # filhos
        montaGrafoRecursivo(ẞ[0],G,DAT,API,MAX,level+1)


def achaGInLisGs(G, Grafos):
    for i in range(len(Grafos)):

        if graphs_equal(Grafos[i],G) :
            return i
    return -1

def achaG(Gs,noh):
    '''acha um nó em uma lista de grafos'''
    #respe = None
    for i in range(len(Gs)):
#    for G in Gs:
        if noh in Gs[i].nodes:
            return Gs[i]
    return None


def MontaGrafosSimilaridade_novo(Gs, Dat, NLP, τ):
    '''TESTAR'''
    Gs_ = []
    # if τ < 0 or τ > 1 :
    #    return Gs

    for G in Gs:
        Gs_.append(deepcopy(G))
    Rels = []

    Þ = []
    for i in range(len(Gs_)):
        Þ.append('claim_' + str(i) + '.html')

    for i in Dat:
        for j in Dat:
            # print(i,j)
            # print(Dat[i])
            # print(Dat[j])
            # i = Dat["id"] #i e j ja sao id
            # j = Dat["id"]
            dhI = Dat[i][3]
            dhJ = Dat[j][3]
            textoI = Dat[i][0]
            textoJ = Dat[j][0]
            Gi = achaG(Gs_, i)
            Gj = achaG(Gs_, j)
            #            print(10*'-')
            #            print(i, Gi, dhI)
            #            print(j, Gj, dhJ)
            #            print(10*'-')
            if AND(i != j, i not in Gj.nodes, j not in Gi.nodes, dhI < dhJ):
                #                print('ÉÉÉÉ')
                Ψ, Φ = NLP(textoI, textoJ)
                θ = Cos_vet(Ψ, Φ)
                if θ >= τ:
                    Rels.append({'i': i, 'j': j, 'Gi': Gi, 'Gj': Gj, 'theta': θ})
    for insercao in Rels:
        Gi = insercao["Gi"]
        Gj = insercao["Gj"]
        j = insercao["j"]
        theta = insercao["theta"]
        i = insercao["i"]

        i_link_Gi = achaGInLisGs(Gi, Gs_)
        i_link_Gj = achaGInLisGs(Gj, Gs_)
        link_Gi = Þ[i_link_Gi]
        link_Gj = Þ[i_link_Gj]

        print(Dat[j])
        Gi.add_node(j,
                    title=converte_conteudo(Dat[j]) + '</br><a href="'+link_Gj+'">[LINK PARA O GRAFO DO CLAIM]</a>',
                    label=str(j) + '\n' + datetime2str(Dat[j][3]) + '\n' + str(round(100 * theta, 2)) + '%',
                    group=50
                    )
        Gj.add_node(i,
                    title=converte_conteudo(Dat[i]) + '</br><a href="'+link_Gi+'">[LINK PARA O GRAFO DO CLAIM]</a>',
                    label=str(i) + '\n' + datetime2str(Dat[i][3]) + '\n' + str(round(100 * theta, 2)) + '%',
                    group=50
                    )
        add_aresta_grafo(Gi, i, j, theta / 5)
        add_aresta_grafo(Gj, i, j, theta / 5)
    return {'Gs':Gs_ , 'links': Þ}


def MontaGrafosSimilaridade(Gs,Dat,NLP,τ,ehJacc):
    '''Cria Cópia de lista de grafos que representam fluxo de mensagens, esta cópia contem grafos
    com arestas adicionais geradas por similaridade inter-claims (inter-grafos)
    como utilizar os vetorizadores
    JACCAND :        J=Jaccand(set(tA.split(' ')),set(tB.split(' ')))
                     RETN J %

    SPACY(WORD2VEC) :K=Corpus_Portug_SpaCy([tA,tB])
                     vA_SpaCy=K[0].vector
                     vB_SpaCy=K[1].vector
                     RETN vA,vB

    TFID    :       vA_TFID=VetorizadorTFid([tA])[0]
                    vB_TFID=VetorizadorTFid([tB])[0]
                    RETN vA,vB

    BOW :           *
    '''
    Gs_ =[]
    #if τ < 0 or τ > 1 :
    #    return Gs

    MaisSimilares=[]

    for G in Gs :
        Gs_.append(deepcopy(G))
    Rels=[]
    for i in Dat :
        for j in Dat :
            #print(i,j)
            #print(Dat[i])
            #print(Dat[j])
            #i = Dat["id"] #i e j ja sao id
            #j = Dat["id"]
            dhI=Dat[i][3]
            dhJ=Dat[j][3]
            textoI=Dat[i][0]
            textoJ=Dat[j][0]
            Gi=achaG(Gs_,i)
            Gj=achaG(Gs_,j)
#            print(10*'-')
#            print(i, Gi, dhI)
#            print(j, Gj, dhJ)
#            print(10*'-')
            if AND(i!=j,i not in Gj.nodes,j not in Gi.nodes,dhI<dhJ):
#                print('ÉÉÉÉ')
                if NLP.__name__ != 'SimilaridadeJaccand' :#ehJacc :
#                if not ehJacc :
                    Ψ, Φ=NLP(textoI,textoJ)
                    θ = Cos_vet(Ψ, Φ)
                    #print(NLP.__name__)
                else:
                    θ = NLP(textoI,textoJ)/100
                    #print(θ)
                if θ >= τ :
                    MaisSimilares.append(i)
                    MaisSimilares.append(j)
                    #print('appendei',i,j)
                    Rels.append({'i':i,'j':j,'Gi':Gi,'Gj':Gj,'theta':θ})
    #print('****passei')
    for insercao in Rels:
        Gi=insercao["Gi"]
        Gj=insercao["Gj"]
        j=insercao["j"]
        theta=insercao["theta"]
        i=insercao["i"]
        #print(Dat[j])
        Gi.add_node(j,
               title=converte_conteudo(Dat[j])+'</br><a href="#$#$#$">[LINK PARA O GRAFO DO CLAIM]</a>',
               label=str(j) + '\n' + datetime2str(Dat[j][3])+ '\n'+str(round(100*theta,2))+'%',
               group=50
               )
        Gj.add_node(i,
               title=converte_conteudo(Dat[i])+'</br><a href="#$#$#$">[LINK PARA O GRAFO DO CLAIM]</a>',
               label=str(i) + '\n' + datetime2str(Dat[i][3])+ '\n'+str(round(100*theta,2))+'%',
               group=50
               )
        add_aresta_grafo(Gi,i,j,theta/5)
        add_aresta_grafo(Gj,i,j,theta/5)
    #print(MaisSimilares)
    MaisSimilares=list(set(MaisSimilares))
    FP_OBJ_SAVE(MaisSimilares,'MaisSimilares_'+NLP.__name__+'_'+str(τ*100)+'.DAT')
    print('MaisSimilares_'+NLP.__name__+'_'+str(τ*100)+'.DAT gerado, tamanho',len(MaisSimilares))
    return Gs_




def ObtemSimilaridades(Gs,Dat,NLP,τ,ehJacc):
    '''Cria Cópia de lista de grafos que representam fluxo de mensagens, esta cópia contem grafos
    com arestas adicionais geradas por similaridade inter-claims (inter-grafos)
    como utilizar os vetorizadores
    JACCAND :        J=Jaccand(set(tA.split(' ')),set(tB.split(' ')))
                     RETN J %

    SPACY(WORD2VEC) :K=Corpus_Portug_SpaCy([tA,tB])
                     vA_SpaCy=K[0].vector
                     vB_SpaCy=K[1].vector
                     RETN vA,vB

    TFID    :       vA_TFID=VetorizadorTFid([tA])[0]
                    vB_TFID=VetorizadorTFid([tB])[0]
                    RETN vA,vB

    BOW :           *
    '''
    Gs_ =[]
    #if τ < 0 or τ > 1 :
    #    return Gs

    MaisSimilares=[]
    taxas=[]
    for G in Gs :
        Gs_.append(deepcopy(G))
    Rels=[]
    if NLP.__name__ == 'VectorizaSpaCy2':
        taxas=NLP(Dat,Gs)
        print('final do nlp ',NLP.__name__)
        FP_OBJ_SAVE(taxas,'taxas_'+NLP.__name__+'.DAT')
        return taxas
    else:
        for i in Dat :
            for j in Dat :
                dhI=Dat[i][3]
                dhJ=Dat[j][3]
                textoI=Dat[i][0]
                textoJ=Dat[j][0]
                Gi=achaG(Gs_,i)
                Gj=achaG(Gs_,j)

                if AND(i!=j,i not in Gj.nodes,j not in Gi.nodes,dhI<dhJ):

                    if NLP.__name__ != 'SimilaridadeJaccand' :#ehJacc :
    #                if not ehJacc :
                        Ψ, Φ=NLP(textoI,textoJ)
                        θ = Cos_vet(Ψ, Φ)

                    else:
                        θ = NLP(textoI,textoJ)/100


                    taxas.append({'i':i,'j':j,'Gi':Gi,'Gj':Gj,'theta':θ})
        print('final do nlp ',NLP.__name__)
        FP_OBJ_SAVE(taxas,'taxas_'+NLP.__name__+'.DAT')
        return taxas

def VectorizaSpaCy2(Dat,Gs):
    '''retorna vetor com todas as taxas de similaridade inter-grafos
    {'i':i,'j':j,'Gi':Gi,'Gj':Gj,'theta':θ}'''
    t=[]
    INDEXt=[]
    for i in Dat:
        t.append(Dat[i][0])
        INDEXt.append(i)
    #print('processando textos')
    K=Corpus_Portug_SpaCy(t)
    resp=[]
    #print('processado, tamanho de K = ',len(K),';; famanho de Dat = ',len(t))
    procs=0
    for i in range(len(K)):
        for j in range(len(K)):
            if i!=j:
                noI=INDEXt[i]
                noJ=INDEXt[j]
                GiINDEX=achaTweetNoGrafo(Gs,noI)
                GjINDEX=achaTweetNoGrafo(Gs,noJ)
                dhI=Dat[noI][3]
                dhJ=Dat[noJ][3]
                Gi=Gs[GiINDEX]
                Gj=Gs[GjINDEX]
                #print('processados  = ',procs,'/',len(K)**2,':','i=',noI,'j=',noJ)
                if GiINDEX != GjINDEX and dhI < dhJ :
                    θ = Cos_vet(K[i].vector,K[j].vector)
                    resp.append({'i':noI,'j':noJ,'Gi':Gi,'Gj':Gj,'theta':θ})
                    #print('''   proecessado''',i,j,'θ=',θ)
            procs=procs+1
    return resp

def montaGrafoPelasTaxas(Rels,Gs,τ,Dat,caso_teste):
    Gs_ =[]
    if τ < 0 or τ > 1 :
        return Gs
    for G in Gs :
        Gs_.append(deepcopy(G))
    # if θ >= τ :
    #    MaisSimilares.append(i)
    #    MaisSimilares.append(j)
    # print('appendei',i,j)
    #    Rels.append({'i':i,'j':j,'Gi':Gi,'Gj':Gj,'theta':θ})
    #print('****passei')
    for insercao in Rels:
        theta = insercao["theta"]
        if theta >= τ :
            j=insercao["j"]
            i=insercao["i"]
            INDEX_Gi=achaTweetNoGrafo(Gs_,i)#insercao["Gj"]
            INDEX_Gj=achaTweetNoGrafo(Gs_,j)#insercao["Gj"]
            #print(Dat[j])
            print('link inserido em ',i,':','claim_'+str(INDEX_Gj)+'_'+caso_teste+'.html')
            print('link inserido em ',j,':','claim_'+str(INDEX_Gi)+'_'+caso_teste+'.html')
            Gs_[INDEX_Gi].add_node(j,
#                   title=converte_conteudo(Dat[j])+'</br><a href="#$#$#$">[LINK PARA O GRAFO DO CLAIM]</a>',
                   title=converte_conteudo(Dat[j])+'</br><a href="claim_'+str(INDEX_Gj)+'_'+caso_teste+'.html">[LINK PARA O GRAFO DO CLAIM]</a>',
                   label=str(j) + '\n' + datetime2str(Dat[j][3])+ '\n'+str(round(100*theta,2))+'%',
                   group=50
                   )
            Gs_[INDEX_Gj].add_node(i,
#                   title=converte_conteudo(Dat[i])+'</br><a href="#$#$#$">[LINK PARA O GRAFO DO CLAIM]</a>',
                   title=converte_conteudo(Dat[i])+'</br><a href="claim_'+str(INDEX_Gi)+'_'+caso_teste+'.html">[LINK PARA O GRAFO DO CLAIM]</a>',
                   label=str(i) + '\n' + datetime2str(Dat[i][3])+ '\n'+str(round(100*theta,2))+'%',
                   group=50
                   )
            add_aresta_grafo(Gs_[INDEX_Gi],i,j,theta/5)
            add_aresta_grafo(Gs_[INDEX_Gj],i,j,theta/5)
        #print(MaisSimilares)
        #MaisSimilares=list(set(MaisSimilares))
        #FP_OBJ_SAVE(MaisSimilares,'MaisSimilares_'+NLP.__name__+'_'+str(τ*100)+'.DAT')
        #print('MaisSimilares_'+NLP.__name__+'_'+str(τ*100)+'.DAT gerado, tamanho',len(MaisSimilares))
    return Gs_




#------------------------------

def drive():
    API = TWITTER(CHAVE())
    DAT = FP_OBJ_OPEN('DAT_seed_tratPrecoce.DAT')
    claimsIds = [
        (1596295439674150912, 'vacina miocardite'),
        (1338290853203341312, 'farsa covid'),
        (1595400013802344449, 'vacina sim'),
        (1598006388718206976, 'fraude eleição')
    ]

    for id, claim in claimsIds:
        G = montaGrafoId(id, 50, API, DAT)
        montaGrafoClaimTwitter(claim, 50, API, DAT, G_existente=G)
        nomeG = claim.replace(' ', '_') + '.GRDAT'
        FP_OBJ_SAVE(G, nomeG)

    FP_OBJ_SAVE(DAT, 'DAT_seed_tratPrecoce.DAT')


def drive2():
    DAT = FP_OBJ_OPEN('DAT_seed_tratPrecoce.DAT')
    claimsIds = [
        (1596295439674150912, 'vacina miocardite'),
        (1338290853203341312, 'farsa covid'),
        (1595400013802344449, 'vacina sim'),
        # (1598006388718206976,'fraude eleição')
    ]
    for id, claim in claimsIds:
        nomeG = claim.replace(' ', '_') + '.GRDAT'
        nomeGHtml = nomeG.replace('.GRDAT', '')
        G = FP_OBJ_OPEN(nomeG)
        print(nomeG)
        Grafo2Mostrador(G, DAT, nomeGHtml, 1000, 800)

def drv():
    API = TWITTER(CHAVE())
    G = FP_OBJ_OPEN('tweet_raiz_1_seed_tratPrecoce.GRDAT')
    POSTS = FP_OBJ_OPEN('DAT_seed_tratPrecoce.DAT')
    ##########montaGrafoClaimTwitter('tratamento precoce salva',50,API,POSTS,G_existente=G)
    ######G=montaGrafoId(1595036532179890177,50,API,POSTS)
    #########FP_OBJ_SAVE(G,'tweet_raiz_1_seed_tratPrecoce.GRDAT')
    #########FP_OBJ_SAVE(POSTS,'DAT_seed_tratPrecoce.DAT')
    ##print('DAT_seed_tratPrecoce.DAT',os.path.exists('DAT_seed_tratPrecoce.DAT'))
    ##print('tweet_raiz_1_seed_tratPrecoce.GRDAT',os.path.exists('tweet_raiz_1_seed_tratPrecoce.GRDAT'))
    # print(POSTS)
    # for key in POSTS:
    #    print(key,key in G.nodes,POSTS[key])

    # print(G.nodes)
    # or n in G.edges:
    #    print(n)
    # for n in G.nodes:
    #    print('''   ''',POSTS[n])
    Grafo2Mostrador(G, POSTS, 'teste34_', 1000, 800)

def drive3():
    a='Japão declara ao mundo que a Ivermectina é mais eficaz que a vacina'
    b='Japão diz ao mundo que a Ivermectina tem maior eficácia em relação a vacina'
    print(a)
    print(b)
    #va=VectorizaBOW(a,b)
    #print(va)
    print('Similaridade Jaccard = ',SimilaridadeJaccand(a,b),'%')
    va,vb=VectorizaBOW(a,b)
    print('Similaridade BOW= ',100*Cos_vet(va,vb),'%')
    #MontaGrafosSimilaridade_novo(Gs,DAT,modelo,0.1)
    #grafico_mapa_calorTFIDFeBOW(CountVectorizer,a,b)

    va,vb=VectorizaTFID(a,b)
    #grafico_mapa_calorTFID_old2(a,b)
    print('Similaridade TFID = ',100*Cos_vet(va,vb),'%')
    #grafico_mapa_calorTFIDFeBOW(TfidfVectorizer,a,b)

    va,vb=VectorizaSpaCy(a,b)
    print('Similaridade Word2Vec = ',100*Cos_vet(va,vb),'%')

    print(50*'=')##########################################

    ###############################RECUPERANDO DADOS JA SALVOS DOS CLAIMS ATE AQUI E OS GRAFOS DE ARQUIVO
    GRARQS=[
        'fraude_eleição.GRDAT'
        ,'vacina_sim.GRDAT'
        ,'tweet_raiz_1_seed_tratPrecoce.GRDAT'
        ,'farsa_covid.GRDAT'
        ,'vacina_miocardite.GRDAT'
    ]
    DAT=FP_OBJ_OPEN('DAT_seed_tratPrecoce.DAT')
    GS=[]
    for GARQ in GRARQS:
        GS.append(FP_OBJ_OPEN(GARQ))
    ###############################RECUPERANDO DADOS JA SALVOS DOS CLAIMS ATE AQUI E OS GRAFOS DE ARQUIVO

    ###################################MONTANDO GRAFOS DE SIMILARIDADE#################################
    #GS_=MontaGrafosSimilaridade(GS,DAT,VectorizaBOW,0.5,False)
    #print('rodei')
    ###################################MONTANDO GRAFOS DE SIMILARIDADE#################################

    #################### MAPA CALOR VETOR SIMILARIDADE ###############################
    DATINDEX=[]
    DATINDEXlabel=[]
    TT=[]
    for i in DAT:
        if not(DAT[i][0].find('RT') >= 0) :
            DATINDEX.append({'no':i,'indexGrafo':achaTweetNoGrafo(GS,i)})
            DATINDEXlabel.append(str(i)+'#Cl'+str(achaTweetNoGrafo(GS,i)))
            TT.append(DAT[i][0])
            #print(i,achaTweetNoGrafo(GS,i),DAT[i])
    print(TT)
    print(DATINDEX)
    grafico_mapa_calorTFID(TT,DATINDEXlabel,'histoData_TFIDF')
    grafico_mapa_calorBOW(TT,DATINDEXlabel,'histoData_BOW')
    grafico_mapa_calorSpaCy(TT,DATINDEXlabel,'histoData_SpaCy')
    #################### MAPA CALOR VETOR SIMILARIDADE ###############################

    ############################MAPA CALOR : OS MAIS SIMILARES##############################
    MAISSIMILARES=FP_OBJ_OPEN('MAISSIMILARES.DAT')
    DATINDEXMaisSimilar=[]
    DATINDEXMaisSimilarLabel=[]
    TTMaisSimilares=[]
    for i in DAT:
        if i in MAISSIMILARES:
            DATINDEXMaisSimilar.append({'no':i,'indexGrafo':achaTweetNoGrafo(GS,i)})
            DATINDEXMaisSimilarLabel.append(str(i)+'#Cl'+str(achaTweetNoGrafo(GS,i)))
            TTMaisSimilares.append(DAT[i][0])
            #print(i,achaTweetNoGrafo(GS,i),DAT[i])
    print(TTMaisSimilares)
    print(DATINDEXMaisSimilar)
    grafico_mapa_calorTFID(TTMaisSimilares,DATINDEXMaisSimilarLabel,'histoDataMaisSim_TFIDF')
    grafico_mapa_calorBOW(TTMaisSimilares,DATINDEXMaisSimilarLabel,'histoDataMaisSim_BOW')
    grafico_mapa_calorSpaCy(TTMaisSimilares,DATINDEXMaisSimilarLabel,'histoDataMaisSim_SpaCy')
    ############################MAPA CALOR : OS MAIS SIMILARES##############################
    return
    ####################### GERANDO MOSTRADORES DE TODOS OS GRAFOS DOS CLAIMS #####################
    for i in range(len(GS_)):
        Grafo2Mostrador(GS_[i],DAT,str(i)+'_BOW',1000,800)
    GS_=MontaGrafosSimilaridade(GS,DAT,None,0.5,True)
    #print('rodei Jaccard')
    #print(GS_)
    #for i in range(len(GS_)):
    #    Grafo2Mostrador(GS_[i],DAT,str(i)+'_Jac',1000,800)
    ####################### GERANDO MOSTRADORES DE TODOS OS GRAFOS DOS CLAIMS #####################


def ObtemMaisSimilares(SIMILS,tau):
    #{'i': i, 'j': j, 'Gi': Gi, 'Gj': Gj, 'theta': θ}
    resp=[]
    for ij in SIMILS:
        if tau >= ij['theta']:
            resp.append(ij['i'])
            resp.append(ij['j'])
    return resp

def HTMLify_grafos_originais(Gs,Dat):
    for i in range(len(Gs)) :
        G=Gs[i]
        Grafo2Mostrador(G,Dat,'Claim_'+str(i),1000,800)
        print('HTML do grafo do claim',i,'/',len(Gs),'gerado')


def HTMLifyClustGrafos(cluster_de_grafos,Dat):
    for i in cluster_de_grafos:
        j = 0
        PCa = cluster_de_grafos[i]
        #print(i)
        for G in PCa:
            #print(G)
            Grafo2Mostrador(G,Dat,'Claim_'+str(j)+'_'+i,1000,800)
            #print('criado','Claim_'+str(j)+'_'+i)
            j=j+1


def statistics(taxas_dat_arq,τ):
    k=0
    DD=FP_OBJ_OPEN(taxas_dat_arq)
    for D in DD:
        if τ <= D['theta'] :
            k=k+1
    return k,len(DD)

def cria_histogramas(SIMILS, τ,Dat,NLP,Gs):
    MAISSIMILARES = ObtemMaisSimilares(SIMILS, τ)  # FP_OBJ_OPEN('MaisSimilares_'+NLP.__name__+'_'+str(τ*100)+'.DAT')
    MAISSIMILARES=list(set(MAISSIMILARES))
    print(NLP.__name__,'x',τ,'Qtd MAIS SIMILARES = ',len(MAISSIMILARES),';;;; qtd similares = ',len(SIMILS))
    # print('\t tentou abrir ','MaisSimilares_'+NLP.__name__+'_'+str(τ*100)+'.DAT')#,'Mais Similares deste =',MAISSIMILARES)
    INDEX_MS = []
    TT_MS = []
    INDEX_MS_label = []
    for i in Dat:
        if i in MAISSIMILARES and not (Dat[i][0].find('RT @') >= 0):
            TT_MS.append(Dat[i][0])
            INDEX_MS_label.append(str(i) + '#Cl' + str(achaTweetNoGrafo(Gs, i)))
            INDEX_MS.append({'no': i, 'indexGrafo': achaTweetNoGrafo(Gs, i)})
    if MAISSIMILARES == []:
        print('Não há nós mais similares do que ', τ * 100, '%', 'para', NLP.__name__)
    else:
        if NLP.__name__ != 'SimilaridadeJaccand':
            if NLP.__name__ == 'VectorizaBOW':
                grafico_mapa_calorBOW(TT_MS, INDEX_MS_label, 'histoDataMaisSim_BOW_' + str(τ * 100))
            if NLP.__name__ == 'VectorizaTFID':
                # print('******',TT_MS)
                grafico_mapa_calorTFID(TT_MS, INDEX_MS_label, 'histoDataMaisSim_TFIDF_' + str(τ * 100))
            if NLP.__name__ == 'VectorizaSpaCy2':
                # print('*')
                grafico_mapa_calorSpaCy(TT_MS, INDEX_MS_label, 'histoDataMaisSim_SpaCy_' + str(τ * 100))


def driver_final(T,Dat,Gs,NLPS,SimilIsPreLoaded,CriarHisto,CriarHTMLSimil,CriarHTML):
    #GRAFOS ORIGINAIS
    if CriarHTML :
        HTMLify_grafos_originais(Gs,Dat)
    #CASOS DE TESTE
    Ca={}

    for NLP in NLPS:
        print('processando NLP = ', NLP.__name__)
        if SimilIsPreLoaded:
            SIMILS = FP_OBJ_OPEN('taxas_'+NLP.__name__+'.dat')
        else:
            SIMILS = ObtemSimilaridades(Gs, Dat, NLP, None, None)#FP_OBJ_OPEN('taxas_VectorizaTFID.DAT')########

        for τ in T :
            print('processando τ=',τ)

            #########OLD#####Ca[NLP.__name__+'_'+str(τ*100)]=MontaGrafosSimilaridade(Gs,Dat,NLP,τ,None) old
            #print('claims = ',len(Gs))
            if CriarHTMLSimil :
                Ca[NLP.__name__+'_'+str(τ*100)]=montaGrafoPelasTaxas(SIMILS,Gs,τ,Dat,NLP.__name__+'_'+str(τ*100))
            #print('sendo guardado grupo de grafos',NLP.__name__+'_'+str(τ*100),'COM QTD DE CLAIMS = ',
            #      len(Ca[NLP.__name__+'_'+str(τ*100)]))
            #print('passei pela montagem do grafo')
            if CriarHisto :
                cria_histogramas(SIMILS, τ,Dat,NLP,Gs)

    if CriarHTMLSimil :
        HTMLifyClustGrafos(Ca, Dat)
    return Ca



#API=TWITTER(CHAVE())
#POSTS=cria_dict_posts()

###drv()
#drive()

#drive3()
def drive4():
    GRARQS=[
        'fraude_eleição.GRDAT'
        ,'vacina_sim.GRDAT'
        ,'tweet_raiz_1_seed_tratPrecoce.GRDAT'
        ,'farsa_covid.GRDAT'
        ,'vacina_miocardite.GRDAT'
    ]
    DAT=FP_OBJ_OPEN('DAT_seed_tratPrecoce.DAT')
    GS=[]
    for GARQ in GRARQS:
        GS.append(FP_OBJ_OPEN(GARQ))
#
    #U= driver_final([.4,.50,.80,.85,.9],DAT,GS,[SimilaridadeJaccand,
    #                                                VectorizaTFID,
    #                                                VectorizaBOW,
    #                                                VectorizaSpaCy2],SimilIsPreLoaded=1,CriarHisto=1,CriarHTML=0,CriarHTMLSimil=1)

    #return driver_final([.47,.8875],DAT,GS,[SimilaridadeJaccand,
    #                                                VectorizaTFID,
    #                                                VectorizaBOW,
    #                                                VectorizaSpaCy2],SimilIsPreLoaded=1,CriarHisto=1,CriarHTML=0,CriarHTMLSimil=0)

    CLAIMS=['fraude eleição','vacina sim','tratamento precoce salva','farsa da covid','vacina causa miocardite']
    for tau in [.4,.50,.80,.85,.9]:
        print(botoesTau(tau))
    print()
    for NLP in [SimilaridadeJaccand,VectorizaTFID,VectorizaBOW,VectorizaSpaCy2]:
        print(botoesNLP(NLP))
    print()
    for i in range (len(CLAIMS)) :
        print(botoesClaim(i,CLAIMS[i]))


#D=FP_OBJ_OPEN('taxas_VectorizaTFID.DAT')
#for key in D:
#    if key['theta'] >=.6:
#        print(key)
RES=drive4()







