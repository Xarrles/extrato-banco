import os
import re
from Config.loguru    import logger
from Libs.loguru      import logger_class
import ofxparse
from Libs.sql import conectar
from unidecode import unidecode
from datetime import datetime 

@logger_class()
class Extrato:

    def __init__(self):
        self.path_ofx = r".\entrada\Extrato-08-01-2025-a-08-02-2025.ofx"

        self.dados = [{valor: str, data: str}]


    def fix_ofx_fitid(self, ofx_file):
        """ Adiciona um FITID único para transações que estejam sem esse campo. """
        with open(ofx_file, "r", encoding="utf-8") as file:
            ofx_content = file.read()

        # Encontrar transações sem FITID e adicionar um identificador único
        fixed_content = re.sub(
            r"<STMTTRN>(.*?)<FITID>\s*</FITID>",
            lambda match: f"{match.group(1)}<FITID>{hash(match.group(1))}</FITID>",
            ofx_content,
            flags=re.DOTALL
        )

        # Criar um novo arquivo corrigido
        name_file = os.path.basename(ofx_file)
        fixed_file = os.path.join(os.path.dirname(ofx_file), "fixed_" + name_file)
        with open(fixed_file, "w", encoding="utf-8") as file:
            file.write(fixed_content)

        return fixed_file


    def extrair(self):

        fixed_ofx = self.fix_ofx_fitid(self.path_ofx)

        with open(fixed_ofx, "r", encoding="ISO-8859-1") as file:
            ofx = ofxparse.OfxParser.parse(file)

        # Exibir informações da conta
        print(f"Banco: {ofx.account.institution}")
        print(f"Conta: {ofx.account.account_id}")
        print(f"Tipo de Conta: {ofx.account.account_type}")
        print(f"Moeda: {ofx.account.statement.currency}")
        
        # Exibir transações
        print("\nTransações:")
        for transaction in ofx.account.statement.transactions:
            print(f"Data: {transaction.date}")
            print(f"Valor: {transaction.amount}")
            print(f"Tipo: {transaction.memo}")
            print(f"Descrição: {transaction.memo}")
            print(f"FITID: {transaction.id}")
            print("-" * 30)


            yield transaction


    def get_strato(self, transaction):
            '''
            Funcao responsavel por descobrir o saldo no momento combase nas transacoes anteriores

            # Dica

            Criar uma variavel global que ira armazenas os saldo com as datas


            Retunr -  soldo
            '''
            saldo == None

            return saldo

    
    def insert_db(self, transction, saldo):
            ...
                sql = """
                INSERT INTO extrato_info (saldo, valor, descricao, tipo, fit_id, mov_data, hora)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

                valores = (0, float(transaction.amount), unidecode(transaction.memo), transaction.memo[:1], int(transaction.id[:10]), "rola", "00:00:00"[:6])
                self.cursor.execute(sql, valores)

                self.db.commit()
            

    def close_db(self):
        self.cursor.close()
        self.db.close()

    def open_db(self):
        self.db = conectar()
        self.cursor = db.cursor()


        
        pass
    def main(self):
        logger.info("\t1.1 -  Extraindo informações do extrato")
        self.open_db()
        for transacao in self.extrair():
             saldo = self.get_strato(transaction=transacao)
             self.insert_db(transction=transacao, saldo=saldo)


        self.close_db()
        cursor.close()
        db.close()
        
        ...