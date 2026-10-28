from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def autenticator():
    """
    Essa é a rota padrão de autenticação do sistemas
    """
    return {
        "mensagem": "voce acessou essa merda",
        "autenticado": False
            
            }