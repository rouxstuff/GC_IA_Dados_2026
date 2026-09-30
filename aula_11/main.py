#random sorteia uma elemento aleatório
import random

cardapio = {'Chocolate': 5.00, 'Vanilla':4.50, 'Morango':3.00, 'Flocos': 9.00, 'Café': 4.50, 'Iced Tea': 14.50, 'Energético':12.99, 'Mocca': 12.00}

brindes = ['Cumpom de desconto 15%','Copo Personalizado', 'Badge']

def mostrar_cardapio():
    print('-- CARDÁPIO --')
    for sabor, preco in cardapio.items():
        print(f'{sabor.title()}, R${preco:.2f}\n')


def fazer_pedido():
    total = 0
    pedido = []
    while True:
        sabor = input('\nSELECIONE O SABOR: (Digite fechar para sair) ')
        if sabor == 'fechar':
            break
        elif sabor in cardapio:
            pedido.append(sabor)
            total += cardapio[sabor]
            print(f'{sabor} adicionado!')
        else:
            print('Esse sabor não esta no cardápio.')
    return pedido, total

mostrar_cardapio()
pedido, total = fazer_pedido()         
print(f'\nSeu pedido: {pedido} foi feito')
print(f'Total: {total:.2f}')

if total > 15:
    print(f'Voce ganhou um brinde: {random.choice[brindes]}')