import os
import re
from Config.loguru    import logger
from Libs.loguru      import logger_class
import ofxparse


@logger_class()
class Extrato:

    def __init__(self):
        self.path_ofx = r".\entrada\Extrato-08-01-2025-a-08-02-2025.ofx"



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
            print(f"Tipo: {transaction.type}")
            print(f"Descrição: {transaction.memo}")
            print(f"FITID: {transaction.id}")
            print("-" * 30)

    def main(self):
        logger.info("\t1.1 -  Extraindo informações do extrato")
        self.extrair()
        ...