from rp.r import *
def main():
    import doge.core
    if random_chance(.1):
        doge.core.main()
    pseudo_terminal(locals(),globals())