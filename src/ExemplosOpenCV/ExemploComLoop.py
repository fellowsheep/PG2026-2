import cv2 as cv
import numpy as np

def menu():
    # Exibir as opcoes do menu aqui
    return input("Escolha uma opção: ")

def main():
    # O código principal do seu programa fica aqui
    img = cv.imread('../../src/ExemplosOpenCV/baboon.png')
    if img is None:
        print("Erro: Não foi possível carregar a imagem. Verifique o caminho.")
        return

    while True:
        opcao = menu()
        cv.destroyAllWindows()
        if opcao == '1':
            # faz o que precisa pra realizar a acao 1
            pass
        elif opcao == '2':
            # faz o que precisa pra realizar a acao 2
            pass
        # ...
        else:
            cv.imshow('Imagem Original', img)
            pass

        # ATENÇÃO ALUNOS: Esta linha é vital para o OpenCV processar a renderização
        # da janela. Como estamos controlando o fluxo pelo input do terminal,
        # uma espera de 1ms é suficiente para atualizar a tela.
        cv.waitKey(1)



if __name__ == "__main__":
    main()