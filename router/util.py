import traceback, sys

def log_exception(e, custom_msg=None, should_print=True):
    _, _, exc_tb = sys.exc_info()
    detailed_exp = traceback.format_exc()
    msg = f"{'Erro.' if custom_msg is None else custom_msg} (Linha {exc_tb.tb_lineno}: {e}).\nErro completo: {detailed_exp}"
    if should_print:
        print(msg)
    return msg
