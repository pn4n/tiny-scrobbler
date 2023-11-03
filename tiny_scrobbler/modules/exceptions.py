from window import W

def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            W.set_status(text=str(e), error=True)
            raise Exception(str(e))
    return wrapper