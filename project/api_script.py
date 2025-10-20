# api_script.py
import requests
import json

def obtener_precio_bitcoin():
    """
    Obtiene el precio actual de Bitcoin
    API pública sin necesidad de API key
    """
    print("\n💰 CONSULTANDO PRECIO DE BITCOIN")
    print("=" * 50)
    
    url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    
    try:
        respuesta = requests.get(url)
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            
            # Extraer información
            precio_usd = datos['bpi']['USD']['rate']
            precio_eur = datos['bpi']['EUR']['rate']
            actualizado = datos['time']['updated']
            
            # Mostrar resultados
            print(f"\n✅ Datos obtenidos exitosamente:")
            print(f"  💵 Precio en USD: ${precio_usd}")
            print(f"  💶 Precio en EUR: €{precio_eur}")
            print(f"  ⏰ Actualizado: {actualizado}")
            
            return datos
        else:
            print(f"❌ Error: {respuesta.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def obtener_usuarios_aleatorios():
    """
    Obtiene usuarios aleatorios para demostración
    API pública sin API key
    """
    print("\n👥 CONSULTANDO USUARIOS ALEATORIOS")
    print("=" * 50)
    
    url = 'https://randomuser.me/api/?results=3'
    
    try:
        respuesta = requests.get(url)
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            usuarios = datos['results']
            
            print(f"\n✅ {len(usuarios)} usuarios obtenidos:\n")
            
            for i, usuario in enumerate(usuarios, 1):
                nombre = f"{usuario['name']['first']} {usuario['name']['last']}"
                email = usuario['email']
                pais = usuario['location']['country']
                
                print(f"{i}. Nombre: {nombre}")
                print(f"   Email: {email}")
                print(f"   País: {pais}\n")
            
            return usuarios
        else:
            print(f"❌ Error: {respuesta.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🚀 SCRIPT DE API EXTERNA")
    print("=" * 50)
    
    # Ejemplo 1: Bitcoin
    bitcoin_data = obtener_precio_bitcoin()
    
    # Ejemplo 2: Usuarios
    usuarios = obtener_usuarios_aleatorios()
    
    print("\n" + "=" * 50)
    print("✅ Script completado exitosamente")
    print("=" * 50 + "\n")