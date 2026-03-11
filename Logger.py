import logging
from logging.handlers import MemoryHandler

def configurar_logging(nombre_app="app", archivo_log="app.log"):
    
    logger = logging.getLogger(nombre_app)
    logger.setLevel(logging.INFO)

    formato = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Handler para archivo (disco)
    file_handler = logging.FileHandler(archivo_log)
    file_handler.setFormatter(formato)

    # Handler en memoria
    memory_handler = MemoryHandler(capacity=1000, target=file_handler)

    logger.addHandler(memory_handler)
    logger.addHandler(file_handler)

    return logger