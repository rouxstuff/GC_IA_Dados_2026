import requests
 
URL_BASE = "https://www.fruityvice.com/api/fruit"
 
print("Bem-vindo ao Consulta Frutas!")
 
while True:
    fruta = input("\nQual fruta você quer consultar? (em inglês, ou 'sair'): ").strip().lower()
 
    if fruta == "sair":
        print("Até mais!")
        break
 
    try:
        resposta = requests.get(f"{URL_BASE}/{fruta}", timeout=10)
 
        if resposta.status_code == 200:
            dados = resposta.json()
            nutri = dados["nutritions"]
 
            print(f"\n {dados['name']} (família {dados['family']})")
            print(f"   Calorias:      {nutri['calories']} kcal")
            print(f"   Açúcar:        {nutri['sugar']} g")
            print(f"   Carboidratos:  {nutri['carbohydrates']} g")
            print(f"   Proteína:      {nutri['protein']} g")
            print(f"   Gordura:       {nutri['fat']} g")
 
        elif resposta.status_code == 404:
            print(f"Não encontrei a fruta '{fruta}'. Tente outra (ex: apple, mango, strawberry).")
 
        else:
            print(f"A API respondeu com status {resposta.status_code}.")
 
    except requests.exceptions.RequestException as erro:
        print(f"Erro de conexão: {erro}")