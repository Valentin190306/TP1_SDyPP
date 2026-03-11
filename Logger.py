import logging
import os


def configurar_logging(nombre_app="app", archivo_log="app.log"):

    carpeta = os.path.dirname(archivo_log)
    if carpeta and not os.path.exists(carpeta):
        os.makedirs(carpeta, exist_ok=True)

    logger = logging.getLogger(nombre_app)
    logger.setLevel(logging.INFO)

    if not logger.handlers:

        formato = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        file_handler = logging.FileHandler(archivo_log)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formato)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formato)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
