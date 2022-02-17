def isFloat(x, check):
    try:
        float(x)
        return check(float(x))
    except ValueError:
        return False
