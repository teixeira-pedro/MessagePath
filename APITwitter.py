import os

import tweepy
from tweepy import API as APITW
from tweepy import TweepyException
#from tweepy_modif_API import API as APITWMOD
import json
from GrafoPost02 import strTwitter2datetime
import pandas as PD
import twitter
from Util import *

def getChave(nome):
    try :
        a=open('TWITTER_'+nome+'.KEY')
        resp=a.read()
        a.close()
        return resp
    except Exception as e:
        print(str(e))
        exit(1)

KEYS = {
"AT": getChave("AT"),
"ATS": getChave("ATS"),
"AK": getChave("AK"),
"AKS":getChave("AKS"),
"BT":getChave("BT")
}

def CHAVE():
    auth = tweepy.OAuth1UserHandler(
        KEYS['AK'], KEYS['AKS'], KEYS['AT'], KEYS['ATS']
    )
    return auth

def TWITTER(CH):
    return tweepy.API(CH)

def TWITTER2(CHS):
    return twitter.Api(
    consumer_key=CHS['AK'],
    consumer_secret=CHS['AKS'],
    access_token_key=CHS['AT'],
    access_token_secret=CHS['ATS'],
    sleep_on_rate_limit=True
)



def Tweets2Pandas(*args):
    liste=[]
    for tw in args:
        liste.extend(tw)
    data = [[tuit.id_str,tuit.user.screen_name,tuit.text,tuit.created_at] for tuit in liste]
    tuites = PD.DataFrame(data,columns=['tweet_id','screen_name','text','timestamp'])
    return tuites

def adic_conversacao_id(PanTweets,API):
    ids=PanTweets.tweet_id
    conversas=[]
    for id in ids:
        TWEET_ID=id
        TWEET_FIELDS='conversation_id'

        try :
            respe= API.request(f'tweets/:{TWEET_ID}', {'tweet.fields': TWEET_FIELDS})
            for item in respe:
                conversas.append(item['conversation_id'])



        except Exception as e:
            print(e)
#        except Exception as Xibu:
#            print('Xibu!!',Xibu)
    print(conversas)
    PanTweets['conversaion_id']=conversas
    return PanTweets


def Tuite(tw):
    #print('#####',tw._json)
    midia=None
    texto=None
    try :
        midia=tw.entities.media.media_url
    except:
        midia=None
    try :
        texto=tw.full_text
    except:
        texto=tw.text
    #rint(tw.created_at,type(tw.created_at))
    return {
                'conteudo':texto,
               'id':tw.id
              , 'autor':tw.user.id
               , 'autor_username':tw.user.screen_name
                ,'autor_nome':tw.user.name
                ,'data':strTwitter2datetime(str(tw.created_at))
                ,'orig':'https://twitter.com/twitter/status/'+str(tw.id)
                ,'anexo':midia
    }




def tweeet2No(*args):
    resp=[]
    for tuite in args:
        #print(tuite)
        resp.append((tuite['id'],{"id":tuite['id'],'conteudo':[#tuite['id'],
                                                              tuite['conteudo'],
                                                              tuite['anexo'],
                                                              0,
                                                              tuite['data'],
                                                              tuite['orig'],
                                                              'user'+str(tuite['autor'])]
                                  }))
    return resp

def retweetEreply2Aresta(*args):
    pass


def getRetweetseReplies(idTweetOrig,api,max):
    if max <=0:
        max= 100
    #os.system('twarc2 conversation'+str(idTweetOriginal)+' > '+idTweetOriginal+'.TWDAT')
    #JSON=json.load(str(idTweetOriginal)+'.TWDAT')
    #print('twarc2 conversation '+str(idTweetOriginal)+' > '+str(idTweetOriginal)+'.RTW')
    arq_replies =   str(idTweetOrig) + '.REP'
    arq_retweets =   str(idTweetOrig) + '.RTW'
    os.system('twarc replies '+str(idTweetOrig)+' > '+arq_replies)
    os.system('twarc retweets '+str(idTweetOrig)+' > '+arq_retweets)
    REPOSTS=[]
    if not os.path.exists(arq_replies):
        return REPOSTS
    FPJ=open(arq_replies)
    temop=FPJ.readlines()[0]
    FPJ.close()
    try:
        JSON = json.loads(temop)
    except Exception as e:
        print(e,'existe(',arq_replies,') = ',os.path.exists(arq_replies))
        return REPOSTS
    for j in JSON['data']:
        #print(j['created_at'])
        REPOSTS.append([(int(j['id']),{"id":int(j['id']),'conteudo':[j['text'],
                                                              None,
                                                              0,
                                                              strReplyTwitter2datetime(j['created_at']),
                                                              'https://twitter.com/twitter/status/'+j['id'],#twOrig['orig'],#twOrig.source_url,
                                                              'user'+str(j['author_id'])]
                                  })])

        #REPLIES.append(tweeet2No(J))
    #MOVER(arq_replies,pasta_orig=os.getcwd(),pasta_dest=os.path.join(os.getcwd(),'data'))
    return REPOSTS



def getRepls(idTweetOrig):
    arq_replies = str(idTweetOrig) + '.RTW'
    os.system('TWARC2 conversation ' + str(idTweetOrig) + ' > ' + arq_replies)
    if not os.path.exists(arq_replies):
        return []
    resp=[]
    fp=open(arq_replies)
    raw=fp.readlines()[0]
    JSON ={}
    try:
        JSON = json.loads(raw)
        print(JSON)
    except Exception as e:
        print(e, 'existe(', arq_replies, ') = ', os.path.exists(arq_replies), 'tentado ', raw)
        # return REPOSTS
        print(raw, '*')
    #print(JSON)
    resp=[]
    if JSON != {}:
        Js=JSON['data']
        print(Js)
        for j in Js:
            texto = ''
            autor = ''
            imagem = None

            try:
                texto = j['text']
            except Exception as e:
                print(e, '*')
                texto = j['full_text']
            try:
                autor = j['author_id']
            except Exception as e:
                print(e, '**')
                autor = j['user']['id']
            try:
                imagem = j['entities']['media']['media_url_https']
            except Exception as e:
                print(e, '***')
                imagem = None
            print(j['created_at'])
            resp.append([(int(j['id']), {"id": int(j['id']), 'conteudo': [texto,
                                                                          imagem,
                                                                          0,
                                                                          str(str(j['created_at'])),
                                                                          'https://twitter.com/twitter/status/' + str(
                                                                              j['id']),
                                                                          # twOrig['orig'],#twOrig.source_url,
                                                                          'user' + str(autor)]
                                         })])

            # REPLIES.append(tweeet2No(J))
        # MOVER(arq_replies,pasta_orig=os.getcwd(),pasta_dest=os.path.join(os.getcwd(),'data'))
    #print(resp)
    return resp


def getRetws(idTweetOrig):
    arq_retweets=str(idTweetOrig) + '.RTW'
    os.system('twarc retweets ' + str(idTweetOrig) + ' > ' + arq_retweets)
    if not os.path.exists(arq_retweets):
        return []
    resp=[]
    temp=open(arq_retweets)
    lis=temp.readlines()
    temp.close()
    for raw in lis:

        JSON={}
        try:
            JSON = json.loads(raw)
            print(JSON)
        except Exception as e:
            print(e,'existe(',arq_retweets,') = ',os.path.exists(arq_retweets),'tentado ',raw)
                #return REPOSTS
            print(raw,'*')
        j=JSON
        if j=={}:
            break
        #print('$$$$$$$$$$$$$$$',j)
        print(j['created_at'])
        texto=''
        autor=''
        imagem=None

        try:
            texto=j['text']
        except Exception as e:
            print(e,'*')
            texto=j['full_text']
        try:
            autor=j['author_id']
        except Exception as e:
            print(e,'**')
            autor=j['user']['id']
        try:
            imagem=j['entities']['media']['media_url_https']
        except Exception as e:
            print(e,'***')
            imagem=None
        print(j['created_at'])
        resp.append([(int(j['id']),{"id":int(j['id']),'conteudo':[texto,
                                                                  imagem,
                                                                  0,
                                                                  strRepRetTwitter2datetime(str(j['created_at'])),
                                                                  'https://twitter.com/twitter/status/'+str(j['id']),#twOrig['orig'],#twOrig.source_url,
                                                                  'user'+str(autor)]
                                      })])

        #REPLIES.append(tweeet2No(J))
    #MOVER(arq_replies,pasta_orig=os.getcwd(),pasta_dest=os.path.join(os.getcwd(),'data'))
    return resp


def getRetweetsEReplies(idTweetOrig,api,max):
    return getRepls(idTweetOrig)+getRetws(idTweetOrig)


def getRetweets(idTweetOrig,api,max):
    '''Obtém retweets ao tweet de id idTweetOriginal, use como exemplo para olhar, o 266031293945503744'''
    if max <=0:
        max= 100
    #os.system('twarc2 conversation'+str(idTweetOriginal)+' > '+idTweetOriginal+'.TWDAT')
    #JSON=json.load(str(idTweetOriginal)+'.TWDAT')
    #print('twarc2 conversation '+str(idTweetOriginal)+' > '+str(idTweetOriginal)+'.RTW')
    os.system('twarc2 conversation '+str(idTweetOrig)+' > r'+str(idTweetOrig)+'.RTW')
    REPLIES=[]
    arq_replies='r'+str(idTweetOrig)+'.RTW' #'conversation.jsonl'
    if not os.path.exists(arq_replies):
        return REPLIES
    FPJ=open(arq_replies)
    temop=FPJ.readlines()[0]
    FPJ.close()
    try:
        JSON = json.loads(temop)
    except Exception as e:
        print(e,'existe(',arq_replies,') = ',os.path.exists(arq_replies))
        return REPLIES
    for j in JSON['data']:
        #print(j['created_at'])
        REPLIES.append([(int(j['id']),{"id":int(j['id']),'conteudo':[j['text'],
                                                              None,
                                                              0,
                                                              strReplyTwitter2datetime(j['created_at']),
                                                              'https://twitter.com/twitter/status/'+j['id'],#twOrig['orig'],#twOrig.source_url,
                                                              'user'+str(j['author_id'])]
                                  })])

        #REPLIES.append(tweeet2No(J))
    MOVER(arq_replies,pasta_orig=os.getcwd(),pasta_dest=os.path.join(os.getcwd(),'data'))
    return REPLIES


def getRetweets_(idTweetOrig,api,max):
    '''[DEPRECIADO : Estoura Limite de tempo para buscar]
    Obtém retweets ao tweet de id idTweetOriginal, use como exemplo para olhar, o 266031293945503744'''
    if max <=0:
        max= 100
    response=api.get_retweets(idTweetOrig,count=max,tweet_mode="extended")
    resp=[]
    for tw in response:
        resp.append(tweeet2No(Tuite(tw)))
    return resp

def getReplies(idTweetOriginal,twOrig):
    '''Obtém respostas ao tweet de id idTweetOriginal, use como exemplo para olhar, o 266031293945503744'''
    #os.system('twarc2 conversation'+str(idTweetOriginal)+' > '+idTweetOriginal+'.TWDAT')
    #JSON=json.load(str(idTweetOriginal)+'.TWDAT')
    #print('twarc2 conversation '+str(idTweetOriginal)+' > '+str(idTweetOriginal)+'.RTW')
    os.system('twarc2 conversation '+str(idTweetOriginal)+' > '+str(idTweetOriginal)+'.RTW')
    REPLIES=[]
    arq_replies=str(idTweetOriginal)+'.RTW' #'conversation.jsonl'
    if not os.path.exists(arq_replies):
        return REPLIES
    FPJ=open(arq_replies)
    temop=FPJ.readlines()[0]
    FPJ.close()
    try:
        JSON = json.loads(temop)
    except Exception as e:
        print(e,'existe(',arq_replies,') = ',os.path.exists(arq_replies))
        return REPLIES
    for j in JSON['data']:
        #print(j['created_at'])
        REPLIES.append([(int(j['id']),{"id":int(j['id']),'conteudo':[j['text'],
                                                              None,
                                                              0,
                                                              strReplyTwitter2datetime(j['created_at']),
                                                              'https://twitter.com/twitter/status/'+j['id'],#twOrig['orig'],#twOrig.source_url,
                                                              'user'+str(j['author_id'])]
                                  })])

        #REPLIES.append(tweeet2No(J))
    MOVER(arq_replies,pasta_orig=os.getcwd(),pasta_dest=os.path.join(os.getcwd(),'data'))
    return REPLIES


def taest555():
    #https://docs.tweepy.org/en/stable/api.html#tweets
    API=TWITTER(CHAVE())
    #API2=tweepy.Client()
    public_tweets = API.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)

    print('*******************************************')
    a=API.get_retweets(1265889240300257280)
    print(a)
    print('*******************************************')
    #tweepy.tweet.Tweet.
    ltwkina=API.search_tweets(id,count=20)
    for tw in ltwkina:
        print('----------------------------------------------------\n')
        print(tw.text,'\n [ID]',tw.id,'\n [autor]',tw.author._json,'\n [dtcr]',tw.created_at,
              '\n [retweets]',tw.retweets(),'\n',tw.retweets,
              '\n [orig]',tw.source_url,'\n [source]',tw.source,'\n [retweeted]',tw.retweeted,
              '\n [retuite contagem]',tw.retweet_count,'\n [user]',tw.user
              #,              '\n[respostas]',getReplies(tw.id,tw.author._json['name'],API)
              )#'\n[anexos]',tw.attachments)
        k=tw.retweets


def taest5550():
    # authorization of consumer key and consumer secret
    auth = tweepy.OAuthHandler(KEYS['AK'], KEYS['AKS'])

    # set access to user's access key and access secret
    auth.set_access_token(KEYS['AT'], KEYS['ATS'])

    # calling the api
    api = tweepy.API(auth)

    # the ID of the tweet
    ID = 1265889240300257280

    # getting the retweeters
    retweets_list = api.retweets(ID)

    # printing the screen names of the retweeters
    for retweet in retweets_list:
        print(retweet.user.screen_name)

#taest555()

def u():
    auth = tweepy.OAuthHandler(KEYS['AK'], KEYS['AKS'])

    # set access to user's access key and access secret
    auth.set_access_token(KEYS['AT'], KEYS['ATS'])
    ID = 1549844998568419330
    API=APITW(auth)
    retweets_list = API.get_retweets(ID)
    #print(retweets_list[0]._json)
    for tw in retweets_list:
#    tw=retweets_list[0]
#    print(tw.text, '\n [ID]', tw.id, '\n [autor]', tw.author._json, '\n [dtcr]', tw.created_at,
#          '\n [retweets]', tw.retweets(), '\n', tw.retweets,
#          '\n [orig]', tw.source_url, '\n [source]', tw.source, '\n [retweeted]', tw.retweeted,
#          '\n [retuite contagem]', tw.retweet_count, '\n [user]', tw.user
#          # ,              '\n[respostas]',getReplies(tw.id,tw.author._json['name'],API)
#          )  # '\n[anexos]',tw.attachments)
    #for retweet in retweets_list:
    #    print(retweet)
        print(Tuite(tw))
        print(tweeet2No(Tuite(tw)))





def taest5556():
    #https://docs.tweepy.org/en/stable/api.html#tweets
    API=TWITTER(CHAVE())
    #API2=tweepy.Client()





    #ltwkina=API.search_tweets(q='cloroquina',count=20,tweet_mode="extended")
    #FP_OBJ_SAVE(ltwkina,'TUITES_TESTE.DAT')
    B=FP_OBJ_OPEN('TUITES_TESTE.DAT')
    print(B)
    ltwkina=B
    print(Tweets2Pandas(ltwkina))
    #TweetsEmPandas=Tweets2Pandas(ltwkina)
    #Tweets_Convertidos=adic_conversacao_id(TweetsEmPandas,API)
    #print(Tweets_Convertidos)


def taest7777():
    #https://docs.tweepy.org/en/stable/api.html#tweets
    API=TWITTER(CHAVE())
    #API2=tweepy.Client()
    public_tweets = API.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)

    print('*******************************************')
    a=FP_OBJ_OPEN('RETWEETS.DAT')#API.get_retweets(1577787727906480128)
    print(a)
    print('*******************************************')
    #tweepy.tweet.Tweet.
    ltwkina=FP_OBJ_OPEN('KINA.DAT')#API.search_tweets(q='cloroquina',count=20)
    for tw in ltwkina:
        print('----------------------------------------------------\n')

        print(tw.text,'\n [ID]',tw.id,'\n [autor]',tw.author,'\n [dtcr]',tw.created_at,'\n [retweets]',tw.retweets,
              '\n [orig]',tw.source_url,'\n [source]',tw.source,'\n [retweeted]',tw.retweeted,
              '\n [retweet]',tw.retweet,'\n [retuite contagem]',tw.retweet_count,'\n [user]',tw.user,
              )#'\n[anexos]',tw.attachments)
    #FP_OBJ_SAVE(a,'RETWEETS.DAT')
    #FP_OBJ_SAVE(ltwkina,'KINA.DAT')




def taest5555():
    #https://docs.tweepy.org/en/stable/api.html#tweets
    API=TWITTER(CHAVE())
    #API2=tweepy.Client()

    #import ssl
    #ssl._create_default_https_context = ssl._create_unverified_context

    #auth=tweepy.OAuthHandler(KEYS['AK'],KEYS['AKS'])
    #auth.set_access_token(KEYS['AT'],KEYS['ATS'])

    #API2=tweepy.API(auth)

    ltwkina=FP_OBJ_OPEN('TUITES_TESTE.DAT')
    #print('*******')
    #T2=TWITTER2(KEYS)
    #ltwkina=API.search_tweets(q='cloroquina',count=20)
    #ltwkina=API.search_tweets(q='id:266031293945503744',include_entities=True,count=5)
    #ltwkina=[API.get_status(id=266031293945503744,include_entities=True)]
    #FP_OBJ_SAVE(ltwkina,'RESP_TESTE2.DAT')
    ltwkina=FP_OBJ_OPEN('RESP_TESTE2.DAT')
    #print('*******')
    #ltwkina=API.
    cont=0
    for tw in ltwkina:

        T=Tuite(tw)
        print('='*80)
        #print(T)


        print('   -----[retuites]-----')
        rt=getRetweets(Tuite(tw)['id'],API,10)
        for i in rt:
            print('''   '''+str(i))
        print('   -----[retuites]-----')
        print('''   ''','-----[respostas]-----')
        rp=getReplies(idTweetOriginal=tw.id,twOrig=tw)
        for i in rp:
            print('''   ''',i)
        #k = getReplies3(Tuite(tw)['id'], T2)
        #k = getReplies(Tuite(tw)['id'],Tuite(tw)['autor_username'],API)
        #print(k)
        #print(getReplies2(idTweetOrig=Tuite(tw)['id'],API=API,autorTweetOrig=None))
        print('''   ''','-----[respostas]-----')

    #print(getRetweets(1549844998568419330, API, 10))
    print('end')
#    tuite=Tuite(ltwkina[0])
 #   nome=tuite['autor_username']
  #  id=str(tuite['id'])
   # print(id,nome)
    #print(tuite)
    #respes=[]
    #for tweet_candidato in tweepy.Cursor(API.search_tweets(q='to:'+nome, result_type='recent', timeout=999999)).items(1000):
    #    if hasattr(tweet_candidato, 'in_reply_to_status_id_str'):
    #        respes.append(tweet_candidato)
    #        print(tweet_candidato)
    # taest555()





#taest5555()
#u()