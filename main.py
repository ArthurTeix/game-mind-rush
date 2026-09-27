import sys

# Corrige bordas/tela cortada no Windows quando há escala de DPI
if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()

from game.motor import Motor


def main():
    iniciar = Motor()
    iniciar.jogo()


if __name__ == '__main__':
    main()
