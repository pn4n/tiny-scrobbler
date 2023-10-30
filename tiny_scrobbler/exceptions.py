from window import W

def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            W.set_status(text=' ', previous_res=str(e))
    return wrapper