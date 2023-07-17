from Util import *
import matplotlib.pyplot as plt

def plot_2d_points(li,titulo,narq_out):
     xs = [x[0] for x in li]
     ys = [x[1] for x in li]
     plt.plot(xs, ys)
     plt.title(titulo)
     plt.savefig(narq_out)

def statistics(taxas_dat_arq,τ):
     k=0
     DD=FP_OBJ_OPEN(taxas_dat_arq)
     for D in DD:
         if τ <= D['theta'] :
             k=k+1
     return k,len(DD)

def Þ(S):
     τ=0.0
     stat=[]
     while τ <= 1:
             stat.append((τ,statistics(S,τ)))
             #print(τ,statistics(S,τ))
             τ=τ+0.025
     return stat


def Þ7(S):
    τ = 0.5
    stat = []
    while τ <= 1:
        stat.append((τ, statistics(S, τ)))
        # print(τ,statistics(S,τ))
        τ = τ + 0.025
    return stat


#JA=FP_OBJ_OPEN('taxas_SimilaridadeJaccand.DAT')
def obtem_graficos():
    for i in ['taxas_SimilaridadeJaccand.DAT','taxas_VectorizaTFID.DAT','taxas_VectorizaBOW.DAT','taxas_VectorizaSpaCy2.DAT']:
        img=i.replace('.DAT','.png')
        plot_2d_points(Þ7(i),'Jaccard - Similaridade τ x Þ Numero de arestas de similaridade',img)
    print('plotado')

results=[]
for i in ['taxas_SimilaridadeJaccand.DAT', 'taxas_VectorizaTFID.DAT', 'taxas_VectorizaBOW.DAT',
          'taxas_VectorizaSpaCy2.DAT']:
    a = open(i+'.AAA', 'w')
    for j in Þ(i):
        a.write(str(j[0])+'###'+str(j[1][0])+'\n')
    a.close()



