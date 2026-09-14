''''
TEMA DO GRUPO: GAMES
    - Elden Ring
    - Condicional
'''
print("-- VERIFICADOR DE ATRIBUTOS --")

cmaxe_atk = {"PHY" : 146, "MAG" : 0, "FIRE" : 0, "HOLY" : 0, "LIGT" : 0, "CRIT" : 100}
cmaxe_def = {"DPHY" : 68, "DMAG" : 36, "DFIRE" : 36, "DHOLY" : 36, "DLIGT" : 36, "BOOST" : 44}

strength = int(input("STRENGTH: "))
dexterity = int(input("DEXTERITY: "))

def validation(strength, dexterity, atk, deff):
    if strength >= 25 and dexterity >= 15:
        print("\nVoce pode usar o Crescent Moon Axe.")
        print(f" -- CRESCENT MOON AXE ATTRIBUTES -- \n"
              f"ATK: {atk['PHY']} | DPHY: {deff['DPHY']}\n"
              f"MAG: {atk['MAG']} | DMAG: {deff['DMAG']}\n"
              f"FIRE: {atk['FIRE']} | DFIRE: {deff['DFIRE']}\n"
              f"HOLY: {atk['HOLY']} | DHOLY: {deff['DHOLY']}\n"
              f"LIGT: {atk['LIGT']} | DLIGT: {deff['DLIGT']}\n"
              f"CRIT: {atk['CRIT']} | BOOST: {deff['BOOST']}")
              
   
    elif strength >= 15 and dexterity == 10:
        print("\nVoce consegue usar o Crescent Moon Axe, mas com limitações.")
        print(f" -- CRESCENT MOON AXE ATTRIBUTES -- \n"
              f"ATK: {int(atk['PHY'])} | DPHY: {int(deff['DPHY'] * 0.5)}\n"
              f"MAG: {atk['MAG']} | DMAG: {deff['DMAG']}\n"
              f"FIRE: {atk['FIRE']} | DFIRE: {deff['DFIRE']}\n"
              f"HOLY: {atk['HOLY']} | DHOLY: {deff['DHOLY']}\n"
              f"LIGT: {atk['LIGT']} | DLIGT: {deff['DLIGT']}\n"
              f"CRIT: {int(atk['CRIT'] * 0.5)} | BOOST: {deff['BOOST']}")
        print("Dano crítico e defesa reduzidos.")
    
    else:
        print("\nVoce não consegue usar o Crescent Moon Axe.")
        print(f"\n MINIMO = STRENGTH: 15 | DEXTERITY: 10 \n RECOMENDADO = STRENGTH: 25 | DEXTERITY: 15 ")

validation(strength, dexterity, cmaxe_atk, cmaxe_def)
