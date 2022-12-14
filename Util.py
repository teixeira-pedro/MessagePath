import os
import pickle
import shutil
from datetime import datetime
import datetime as DTT


def FP_OBJ_SAVE(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

def FP_OBJ_OPEN(filename):
    with open(filename,'rb') as FP:
        data=pickle.load(FP)
    return data

def datetime2str(dt):
    'pega um datetime e passa pra string'
    assert type(datetime.now()==dt)
    return str(dt).split('.')[0]

def criaDataHora(dd,MM,aa,hh,mm):
    return DTT.datetime(year=aa,day=dd,month=MM,hour=hh,minute=mm,second=0)


def datetime2strTwitter(dt):
    'pega um datetime e passa pra string formato twitter 2022-10-05 22:36:00+00:00'
    return datetime2str(dt)+'+00:00'

def dataQualquer():
    from random import randint
    import random
    mes=random.choice(tuple(range(1,13)))
    dia=random.choice(tuple(range(1,29)))
    ano=random.choice(tuple(range(1900,2101)))
    return DTT.datetime(year=ano,day=dia,month=mes)

def strReplyTwitter2datetime(s):
    '''Formato padrão twitter das strings de data e hora 2022-11-14T02:09:14.000Z'''
    s=s.split('.')[0]
    dt,h=s.split('T')
    aa,MM,dd=dt.split('-')
    hh,mm,ss=h.split(':')
    aa=int(aa)
    MM=int(MM)
    dd=int(dd)
    hh=int(hh)
    mm=int(mm)
    ss=int(ss)
    return DTT.datetime(year=aa,month=MM,day=dd,hour=hh,minute=mm,second=ss)
def achaMes(s):
    if s=='jan':
        return 1
    if s=='feb':
        return 2
    if s=='mar':
        return 3
    if s=='apr':
        return 4
    if s=='may':
        return 5
    if s=='jun':
        return 6
    if s=='jul':
        return 7
    if s=='aug':
        return 8
    if s=='sep':
        return 9
    if s=='oct':
        return 10
    if s=='nov':
        return 11
    if s=='dec':
        return 12

def strRepRetTwitter2datetime(s):
    LD=s.split(' ')
    diasemana=LD[0]
    MM=achaMes(LD[1].lower())
    dd=LD[2]
    h=LD[3]
    fuso=LD[4]
    aa=LD[5]
    '''Formato padrão twitter das strings de data e hora Sun Nov 20 02:44:58 +0000 2022'''
    s=s.split('.')[0]
    #dt,h=s.split('T')
    aa,MM,dd#=dt.split('-')
    hh,mm,ss=h.split(':')
    aa=int(aa)
    MM=int(MM)
    dd=int(dd)
    hh=int(hh)
    mm=int(mm)
    ss=int(ss)
    return DTT.datetime(year=aa,month=MM,day=dd,hour=hh,minute=mm,second=ss)


def strTwitter2datetime(s):
    '''Formato padrão twitter das strings de data e hora 2022-10-05 22:36:00+00:00'''
    s=s.split('+')[0]
    dt,h=s.split(' ')
    aa,MM,dd=dt.split('-')
    hh,mm,ss=h.split(':')
    aa=int(aa)
    MM=int(MM)
    dd=int(dd)
    hh=int(hh)
    mm=int(mm)
    ss=int(ss)
    return DTT.datetime(year=aa,month=MM,day=dd,hour=hh,minute=mm,second=ss)

def str2Datetime(s):
    dt,h=s.split(' ')
    aa,MM,dd=dt.split('-')
    hh,mm,ss=h.split(':')
    aa=int(aa)
    MM=int(MM)
    dd=int(dd)
    hh=int(hh)
    mm=int(mm)
    ss=int(ss)
    return DTT.datetime(year=aa,month=MM,day=dd,hour=hh,minute=mm,second=ss)


def AND(*A):
    for i in A:
        if not i:
            return False
    return True

def push(pil,i):
    assert type([])==type(pil)
    return pil+[i]

def pop(pil):
    assert type([]) == type(pil)
    if pil==[]:
        return None
    return pil.pop()

def top(pil):
    assert type([]) == type(pil)
    if pil==[]:
        return None
    return pil[0]

def OR(*A):
    r=False
    for i in A:
        r=i or r
    return bool(r)

def TIPOIGUAL(A,B):
    return type(A)==type(B)

def len_sublistas(l):
    assert TIPOIGUAL(l,[])
    resp=[]
    for i in l:
        resp.append(len(i))

def htmlizaImg(path):
    assert AND(TIPOIGUAL(path,""),path!="")
    return '<img src="'+path+'" height="90px" >'



def MOVER(*arqs,pasta_orig,pasta_dest):
    if AND(not os.path.exists(pasta_orig),not os.path.exists(pasta_dest)) :
        return -1,'Pasta origem ou destino nao existe'
    movidos=0
    excecoes=[]
    for arq in arqs:
        try:
            shutil.move(os.path.join(pasta_orig,arq),os.path.join(pasta_dest,arq))
            movidos = movidos +1
        except Exception as e:
            excecoes.append(str(e))
    return movidos,excecoes





