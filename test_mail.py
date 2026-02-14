import asyncio
from core.email_config import send_email

async def test():
    try:
        print("Intentando enviar correo de prueba...")
        await send_email("correo@gmail.com", "Prueba", "Si lees esto, funciona")
        print("¡Enviado con éxito!")
    except Exception as e:
        print(f"Error detectado: {e}")

if __name__ == "__main__":
    asyncio.run(test())