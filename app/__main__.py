from Config             import *
from Config             import logger, show_config
from Libs.loguru        import logger_start
from Modules.extrado    import Extrato

@logger_start
def main():

    extrato = Extrato()

    logger.info("1.0 - Extrai informações do extrato")
    extrato.main()
    ...

if __name__ ==  "__main__":
    show_config()
    main()



    

    
    


