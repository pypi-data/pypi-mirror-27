def _congo(f):
    def wrapper():
        state = f()
        if(state[0] == state[1]):
            print(f.__name__,": Pass")
        else:
            print(f.__name__,": Fail")
    return wrapper