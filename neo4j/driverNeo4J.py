import logging

from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

uri = "neo4j+ssc://5ec34d12.databases.neo4j.io"
user = "neo4j"  # Substitua pelo nome de usuário do seu banco de dados
password = "FUbMP2IVEjHfnzNfYS2GaBFH8j_ATvA-Hi2RxtiRNE0"  # Substitua pela senha do seu banco de dados

ID_COUNT = 1000

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def cria_Id(self):
        global ID_COUNT
        ID_COUNT += 1
        return str(ID_COUNT)

    def criar_no(self, conteudo, anexo, rede_social, timestamp, hyperlink, id_usuario):
        with self.driver.session(database="neo4j") as session:
            id = self.cria_Id()
            result = session.execute_write(
                self._cria_e_retorna_no, id, conteudo, anexo, rede_social, timestamp, hyperlink, id_usuario)
            for record in result:
                print("Criou nó: {no}"
                      .format(no=record['no']))
                return id

    def criar_aresta_reacao(self, id_no1, id_no2):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self._cria_e_retorna_aresta, id_no1, id_no2, 1, "REAÇÃO A")
            for record in result:
                print("Criou aresta entre: {no1}, {no2}"
                      .format(no1=record['no1'], no2=record['no2']))
                
    def criar_aresta_similar(self, id_no1, id_no2, peso_aresta):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self._cria_e_retorna_aresta, id_no1, id_no2, peso_aresta, "SIMILAR A")
            for record in result:
                print("Criou aresta entre: {no1}, {no2}"
                      .format(no1=record['no1'], no2=record['no2']))

    @staticmethod
    def _cria_e_retorna_aresta(tx, id_no1, id_no2, peso_aresta, relacao):
        query = (
            "MATCH (no1:Claim {idNode: $id_no1}), (no2:Claim {idNode: $id_no2}) "
            "CREATE (no1)-[r:`" + relacao + "`]->(no2) "
            "SET r.weight = $peso "
            "RETURN no1, no2"
        )

        result = tx.run(query, id_no1=id_no1, id_no2=id_no2, peso = peso_aresta)
        try:
            return [{"no1": record["no1"], "no2": record["no2"]}
                    for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    @staticmethod
    def _cria_e_retorna_no(tx, id, conteudo, anexo, rede_social, timestamp, hyperlink, id_usuario):
        query = (
            "CREATE (no:Claim { idNode: $id, conteudo: $conteudo, anexo: $anexo, rede_social: $rede_social, timestamp: $timestamp, hyperlink: $hyperlink, id_usuario: $id_usuario}) "
            "RETURN no"
        )
        result = tx.run(query, id=id, conteudo=conteudo, anexo=anexo, rede_social=rede_social, timestamp=timestamp, hyperlink=hyperlink, id_usuario=id_usuario)
        try:
            return [{"no": record["no"]}
                    for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def encontra_no(self, id):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_read(self._encontra_e_retorna_no, id)
            for record in result:
                print("Encontrou nó: {record}".format(record=record))

    @staticmethod
    def _encontra_e_retorna_no(tx, id):
        query = (
            "MATCH (no:Claim) "
            "WHERE no.idNode = $id"
            "RETURN no"
        )
        result = tx.run(query, id=id)
        try:
            return [{"no": record["no"]}
                    for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    @staticmethod
    def retornaIdNo(element_id):
        return element_id.split(":")[2]


if __name__ == "__main__":
    app = App(uri, user, password)
    id1 = app.criar_no(conteudo="Ivermectina salva mais que vacina que causa miocardite eoutras complicações... vacina anticovid é fraude,é genocída", anexo="", rede_social="Twitter", timestamp="2022-11-26 00:11:05", hyperlink="t.co/celnt5mlLg", id_usuario="1585991008")
    print(id1)
    id2 = app.criar_no(conteudo="Japão declara ao mundo que a Ivermectina é mais eficaz que a vacina Remédio este, defendido como tratamento precoce", anexo="", rede_social="Twitter", timestamp="2022-11-22 12:48:38", hyperlink="t.co/67RI1mvKKN", id_usuario="1407654130")
    app.criar_aresta_reacao(id1, id2)
    id3 = app.criar_no(conteudo="Ivermectina salva mais que vacina que causa miocardite eoutras complicações... vacina anticovid é fraude,é genocída", anexo="", rede_social="Twitter", timestamp="2022-11-27 00:11:05", hyperlink="t.co/celnt5mlLg", id_usuario="1585991008")
    id4 = app.criar_no(conteudo="Japão declara ao mundo que a Ivermectina é mais eficaz que a vacina Remédio este, defendido como tratamento precoce", anexo="", rede_social="Twitter", timestamp="2022-11-28 12:48:38", hyperlink="t.co/67RI1mvKKN", id_usuario="1407654130")
    app.criar_aresta_similar(id1, id3, 0.90)
    app.criar_aresta_reacao(id2, id4)
    app.criar_aresta_similar(id3, id2, 0.30)
    app.close()
