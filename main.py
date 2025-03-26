from menus import menus
import os


def exibir_menu(titulo, opcoes):
    """Função para exibir o menu com opções."""
    os.system("cls" if os.name == "nt" else "clear")
    
    
    print("=" * 50)
    print(f"{titulo} (Windows)")
    print("=" * 50)

    for chave, opcao in opcoes.items():
        print(f"{chave}️⃣  {opcao[0]}")
    
    print("\n" + "=" * 50)

def menu_principal():
    opcoes_principais = {
        "1": ("Fazer download dos arquivos das eleições", menus.menu_ano),
       ##"2": ("Gerar Arquivos CSV com votos nominais", menus.menu_normalizar),
        "6": ("Sair", None)
    }
    
    while True:
        exibir_menu("Sistema de resultados de eleições", opcoes_principais)

        escolha = input("👉 Digite o número correspondente: ")

        if escolha in opcoes_principais:
            if escolha == "6":
                print("\n👋 Saindo... Até logo!\n")
                break
            else:
                opcoes_principais[escolha][1]()
        else:
            print("\n❌ Opção inválida! Tente novamente.\n")
            input("Pressione ENTER para continuar...")

menu_principal()
