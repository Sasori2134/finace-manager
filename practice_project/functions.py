def check_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False