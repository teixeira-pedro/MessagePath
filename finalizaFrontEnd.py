def botoesNLP(i):
    base = '''<button name="NLP_%%" type="button" onclick="selectNLP('%%')">%%</button>'''.replace('%%',i.__name__)
    return base



def botoesClaim(i,nomeclaim):
    base = '''<button name="claim_%%" type="button" onclick="selectClaim('%%')">%N%</button><br />'''.replace('%%',str(i)).replace('%N%',nomeclaim)
    return base

def botoesTau(i):
    base = '''<button name="tau_%%" type="button" onclick="selectTau('%%')">%% % similar</button>'''.replace('%%',str(i*100))
    return base





