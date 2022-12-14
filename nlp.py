#https://raisler-voigt.medium.com/estimando-a-similaridade-entre-textos-de-um-jeito-simples-usando-python-6c84a819f1c0

import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
#from matplotlib_venn import venn2
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from numpy.linalg import norm
from pandas import DataFrame
from math import nan

def taest1(vect,test,t1,t2,vocab):
    #t1 e t2 são nossos dois textos, e aplicaremos a real transformação!
    textos = vect.fit_transform([t1, t2])
    textos = test.toarray() #transformando em array para olhar a matriz
    print(test)
    vocab.vocabulary_

#https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction
def similarid_cos(t1,t2,analisador,ngramRange):
    vetor=CountVectorizer(analyzer=analisador,ngram_range=ngramRange)
    resultado=[]
    for pal1 in t1:
        for pal2 in t2:
            x1,x2 =  vetor.fit_transform([pal1,pal2])
            TT1,TT2=x1.toarray(),x2.toarray()

            min=np.amin([TT1,TT2],axis=0)
            soma=np.sum(min)
            cont=np.sum([TT1,TT2][0])
            media=soma/cont
            resultado.append(media)


def medidor_de_similaridade(text1, text2):
    text1=[text1]
    text2=[text2]
    to_vect = CountVectorizer(analyzer='word', ngram_range=(1, 2))
    result = []
    for comentario1 in text1:
        for comentario2 in text2:
            x1, x2 = to_vect.fit_transform([comentario1, comentario2])
            t1, t2 = x1.toarray(), x2.toarray()

            min = np.amin([t1, t2], axis=0)
            sumA = np.sum(min)
            #print(t1)
            #print(t2)
            count = np.sum([t1, t2][0])
            to_mean = sumA / count
            result.append(to_mean)
    return result[0]*100
#------------------------UTIL-----------------------------------

def Jaccand(TT1,TT2):
    T1_n_T2=set.intersection(TT1,TT2)
    T1_u_T2=set.union(TT1,TT2)
    return float(len(T1_n_T2)/len(T1_u_T2))

def prod_interno_vet(u,v):

    return sum(t1_i*t2_i for t1_i,t2_i in zip(u,v))

def Cos_vet(t1,t2):
    #print('₢₢₢₢₢',norm(t1)*norm(t2),prod_interno_vet(t1,t2))
    if norm(t1)*norm(t2) == 0 :
        return nan
    return abs(prod_interno_vet(t1,t2)/(norm(t1)*norm(t2)))

def grafico_mapa_calor_old(MSimil,labels,cmap="YlGnBu"):
    '''depreciado'''
    graf=DataFrame(MSimil)
    graf.columns=labels
    graf.index=labels
    Img, Eixo = plt.subplots(figsize=(6,6))
    sns.heatmap(graf,cmap=cmap)

def grafico_mapa_calor_old2(X,ccpp,cmap="YlGnBu"):
    arr = X.toarray()
    print(arr)
    labels = ccpp[0].split(' ')

    df = pd.DataFrame(cosine_similarity(arr))
    df.columns = labels
    df.index = labels
    fig, ax = plt.subplots(figsize=(5, 5))
    MAPA=sns.heatmap(df, cmap=cmap)
    FIG=MAPA.get_figure()
    FIG.savefig('fig.png')

def grafico_mapa_calorTFID_old3(tA,tB,cmap="YlGnBu"):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([tA,tB])
    arr=X.toarray()

    labels = [headline[:20] for headline in [tA,tB]]

    df = pd.DataFrame(cosine_similarity(arr))
    df.columns = labels
    df.index = labels
    fig, ax = plt.subplots(figsize=(5, 5))
    MAPA=sns.heatmap(df, cmap=cmap)
    FIG=MAPA.get_figure()
    FIG.savefig('fig.png')

def grafico_mapa_calorTFID(ts,DATINDEX,narq,cmap="YlGnBu"):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(ts)
    arr=X.toarray()

    #labels = [headline[:20] for headline in ts]
    labels=DATINDEX
    df = pd.DataFrame(cosine_similarity(arr))
    df.columns = labels
    df.index = labels
    fig, ax = plt.subplots(figsize=(20, 20))
    MAPA=sns.heatmap(df, cmap=cmap)
    FIG=MAPA.get_figure()
    FIG.savefig(os.path.join(os.path.join(os.getcwd(),'data'),narq+'.png'))

def grafico_mapa_calorBOW(ts,DATINDEX,narq,cmap="YlGnBu"):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(ts)
    arr=X.toarray()

    #labels = [headline[:20] for headline in ts]
    labels=DATINDEX
    df = pd.DataFrame(cosine_similarity(arr))
    #print(arr)
    df.columns = labels
    df.index = labels
    fig, ax = plt.subplots(figsize=(20, 20))
    MAPA=sns.heatmap(df, cmap=cmap)
    FIG=MAPA.get_figure()
    FIG.savefig(os.path.join(os.path.join(os.getcwd(),'data'),narq+'.png'))

def grafico_mapa_calorSpaCy(ts,DATINDEX,narq,cmap="YlGnBu"):
#$$$$$$
    #print('passei ******')
    nlp = spacy.load('pt_core_news_lg')
    resp = []
    for linha in ts:
        #print(nlp(linha).vector,linha)
        resp.append(nlp(linha).vector)
    #return resp

    #K = Corpus_Portug_SpaCy([tA, tB])
    #vA_SpaCy = K[0].vector
    #vB_SpaCy = K[1].vector
    #return vA_SpaCy, vB_SpaCy

    #vectorizer = CountVectorizer()
    #X = vectorizer.fit_transform(ts)
    #arr=X.toarray()

    ##labels = [headline[:20] for headline in ts]
    labels=DATINDEX
    print(resp)
    df = pd.DataFrame(cosine_similarity(resp))
    df.columns = labels
    df.index = labels
    fig, ax = plt.subplots(figsize=(20, 20))
    MAPA=sns.heatmap(df, cmap=cmap)
    FIG=MAPA.get_figure()
    FIG.savefig(os.path.join(os.path.join(os.getcwd(),'data'),narq+'.png'))


def VectorizaSpaCy(tA,tB):
    K = Corpus_Portug_SpaCy([tA, tB])
    vA_SpaCy = K[0].vector
    vB_SpaCy = K[1].vector
    return vA_SpaCy, vB_SpaCy


def VectorizaTFID(tA,tB):
    vA_TFID = VetorizadorTFid([tA])[0]
    vB_TFID = VetorizadorTFid([tB])[0]
    return vA_TFID,vB_TFID






def VectorizaBOW(tA,tB):
    Vct=CountVectorizer()
    X=Vct.fit_transform([tA,tB])
    #Y=Vct.fit_transform(tB)
    XX=X.toarray()
    #v,w=
    #w= Y.toarray()
    return  XX[0],XX[1]#v,w


def SimilaridadeJaccand(tA,tB):
    J = Jaccand(set(tA.split(' ')), set(tB.split(' ')))
    return J*100

#------------------------UTIL-----------------------------------

#----------------------CORPUS--------------------------------

def DownloadCorpusPortugSpaCy(pythonPath='C:\\Users\\pedro\\AppData\\Local\\Programs\\Python\\Python37\\python.exe'):
    #os.system(pythonPath+' -m spacy download en_core_web_md')
    #os.system(pythonPath+' -m spacy download pt_core_news_sm')
    os.system(pythonPath+' -m spacy download pt_core_news_lg')

def Corpus_Portug_SpaCy(input):
    '''https://spacy.io/models/pt#pt_core_news_lg'''
    #nlp = spacy.load('pt_core_web_md')
    #nlp = spacy.load('pt_core_news_sm')
    nlp = spacy.load('pt_core_news_lg')
    resp = []
    for linha in input:
        resp.append(nlp(linha))
    return resp



#----------------------CORPUS--------------------------------

#------------------------IA-----------------------------------
def VetorizadorBowCount(t):
    Vct=CountVectorizer()
    X=Vct.fit_transform(t)
    v= X.toarray()
    return v

def VetorizadorTFid(t):
    Vct=TfidfVectorizer()
    X=Vct.fit_transform(t)
    v= X.toarray()
    return v



#------------------------IA-----------------------------------





def taest3():
    '''https://newscatcherapi.com/blog/ultimate-guide-to-text-similarity-with-python'''
    A="Dependendo da natureza do negócio e da teia de constituintes que o embasam"
    B="da natureza do negócio e da teia de constituintes"
    AA='''Dependendo da natureza do negócio e da teia de constituintes que o embasam, 
    pode-se detectar a existência de burocratas, técnicos e outros atores engajados em projetos
     e ideias que, para eles, fazem sentido e pelos quais lutam, mesmo que ainda não os tenham materializado,
      e às vezes, somente se configurando como uma mera agenda, cuja conformação e evolução está sujeita 
      a códigos de conduta, a fontes de poder, ao compartilhamento de uma linguagem comum, a um ambiente
       propício à colaboração e a mecanismos de difusão da inovação tecnológica'''
    BB = '''Dependendo da natureza do negócio e da teia de constituintes que o embasam,
     pode-se detectar a existência de burocratas, técnicos e outros atores engajados em projetos 
     e ideias que, para eles, fazem sentido e pelos quais lutam, mesmo que ainda não os tenham materializado,
      e às vezes, somente se configurando como uma mera agenda, cuja conformação e evolução está sujeita 
      a códigos de conduta, a fontes de poder, ao compartilhamento de uma linguagem comum, a um ambiente 
      propício à colaboração e a mecanismos de difusão da inovação entre as comunidades ocupacionais 
      com que se relacionam'''
    C='A função também serve para medir a similaridade de listas de textos'
    D='do observador avaliar e fazer vários testes, com frases grandes, textos, utilizar'
#    print(similarid_cos(A,B,'word',(1,2)))
    #print(similarid_cos(AA,BB,'word',(1,2)))
    print(C)
    print(D)
    print(medidor_de_similaridade(C,D))
    print(50*'-')
    E='A função tem como objetivo também, a de medição de similaridade de listas textuais'
    print(C)
    print(E)
    print(medidor_de_similaridade(C,E))
    print('-'*20+'SPACY'+'-'*20)
    a=Corpus_Portug_SpaCy([C,D])
    print(a[0].vector)
    print(a[1].vector)
    print('-'*20+'TFID'+'-'*20)

    vTFID=VetorizadorBowCount([AA,BB])
    print(vTFID)
    print('-'*20+'BOW'+'-'*20)

    vBOW=VetorizadorBowCount([AA,BB])
    print(vBOW)
    print('-'*20+'JACCAND'+'-'*20)

    J=Jaccand(set(AA.split(' ')),set(BB.split(' ')))
    print(J)


def taest4():
    F,G='O homem mordeu o cachorro','o cachorro mordeu o homem'
    C='A função também serve para medir a similaridade de listas de textos'
    E='A função tem como objetivo também, a de medição de similaridade de listas textuais'
    tA='O copo está vazio'
    tB ='Não há nada no copo'
    #tA,tB=C,E
    #tA,tB=F,G
    print('"',tA,'" versus "','''
    ''',tB,'"')
    print('-'*20+'JACCAND'+'-'*20)

    J=Jaccand(set(tA.split(' ')),set(tB.split(' ')))
    print(100*round(J,3),' % similares')
    
   # print('-'*20+'BOW'+'-'*20)
   # vA_BOW=VetorizadorBowCount([tA])[0]
   # vB_BOW=VetorizadorBowCount([tB])[0]
   # #print(vB_BOW,vB_BOW)
   # print(100*round(Cos_vet(vA_BOW,vB_BOW),3),' % similares')

    print('-'*20+'SPACY'+'-'*20)
    K=Corpus_Portug_SpaCy([tA,tB])
    vA_SpaCy=K[0].vector
    vB_SpaCy=K[1].vector
    #print(vA_SpaCy,vB_SpaCy)
    print(100*round(Cos_vet(vA_SpaCy,vB_SpaCy),3),' % similares')


    print('-'*20+'TFID'+'-'*20)

    vA_TFID=VetorizadorTFid([tA])[0]
    vB_TFID=VetorizadorTFid([tB])[0]
    print(100*round(Cos_vet(vA_TFID,vB_TFID),3),' % similares')


#DownloadCorpusPortugSpaCy()
#taest3()

#taest4()
