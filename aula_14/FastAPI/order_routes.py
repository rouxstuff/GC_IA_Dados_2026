from fastapi import APIRouter

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/") #endpoint padrão
async def orders():
    """
        Essa é a rota padrão de pedidos do sistemas.
    """
    return {'mensagem': 'voce acessou essa merda'}

