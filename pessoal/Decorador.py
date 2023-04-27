import time
from pessoal.Escriba import registrador

r = registrador()
logger =r.get_logger()

def tempo_decorrido(funcao):
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = funcao(*args, **kwargs)
        fim = time.time()
        logger.info(f'{funcao.__name__} levou {fim - inicio:.5f} segundos para executar.')
        return resultado
    return wrapper
