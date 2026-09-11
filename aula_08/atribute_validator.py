''''
TEMA DO GRUPO: GAMES
    - Elden Ring
    - Condicional
'''
print("-- VERIFICADOR DE ATRIBUTOS --")
strength = int(input("STRENGTH: "))
dexterity = int(input("DEXTERIRY: "))
def validation(strenght, dexteriry):
    if strength >= 25 and dexterity >= 15:
        print("Voce pode usar o Crescent Moon Axe.")
    elif strength >= 15 and dexterity == 10:
        print("Voce consegue usar o Crescent Moon Axe, mas com limitaçãoes.")
    else:
        print("Voce não consegue usar o Crescent Moon Axe.");


validation(strength,dexterity)

