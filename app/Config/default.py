from dotenv import load_dotenv
import locale

#CARREGA VARIAVEIS DE AMBIENTE
load_dotenv("./_.env",override=False)
#CONFIGURA O IDIOMA
locale.setlocale(locale.LC_TIME, 'pt_BR')

