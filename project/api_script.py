# api_script.py
import requests
import json
from datetime import datetime

class CryptoAnalyzer:
    """
    Analiza datos de criptomonedas desde CoinGecko API
    API gratuita sin necesidad de API key
    """
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
    
    def obtener_precios_actuales(self):
        """Obtiene precios actuales de las principales criptomonedas"""
        print("\n" + "="*60)
        print("ANÁLISIS DE MERCADO DE CRIPTOMONEDAS")
        print("="*60)
        
        url = f"{self.base_url}/simple/price"
        params = {
            'ids': 'bitcoin,ethereum,cardano,solana,polkadot',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_market_cap': 'true',
            'include_24hr_vol': 'true'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            datos = response.json()
            
            print(f"\nFecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            for crypto, info in datos.items():
                print(f"\n{crypto.upper()}")
                print("-" * 40)
                print(f"  Precio:           ${info['usd']:,.2f}")
                print(f"  Cambio 24h:       {info['usd_24h_change']:+.2f}%")
                print(f"  Cap. Mercado:     ${info['usd_market_cap']:,.0f}")
                print(f"  Volumen 24h:      ${info['usd_24h_vol']:,.0f}")
            
            return datos
        
        except requests.exceptions.RequestException as e:
            print(f"\nError al obtener datos: {e}")
            return None
    
    def obtener_datos_historicos(self, crypto_id='bitcoin', dias=7):
        """Obtiene datos históricos y calcula estadísticas"""
        print(f"\n\n{'='*60}")
        print(f"DATOS HISTÓRICOS - {crypto_id.upper()} (Últimos {dias} días)")
        print("="*60)
        
        url = f"{self.base_url}/coins/{crypto_id}/market_chart"
        params = {
            'vs_currency': 'usd',
            'days': dias
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            datos = response.json()
            
            # Extraer precios
            precios = [precio[1] for precio in datos['prices']]
            
            # Calcular estadísticas
            precio_min = min(precios)
            precio_max = max(precios)
            precio_promedio = sum(precios) / len(precios)
            volatilidad = ((precio_max - precio_min) / precio_promedio) * 100
            
            print(f"\nEstadísticas de {crypto_id.upper()}:")
            print("-" * 40)
            print(f"  Precio mínimo:    ${precio_min:,.2f}")
            print(f"  Precio máximo:    ${precio_max:,.2f}")
            print(f"  Precio promedio:  ${precio_promedio:,.2f}")
            print(f"  Volatilidad:      {volatilidad:.2f}%")
            print(f"  Rango de precio:  ${precio_max - precio_min:,.2f}")
            
            # Análisis de tendencia
            precio_inicial = precios[0]
            precio_final = precios[-1]
            cambio_porcentual = ((precio_final - precio_inicial) / precio_inicial) * 100
            
            print(f"\nTendencia ({dias} días):")
            print("-" * 40)
            print(f"  Precio inicial:   ${precio_inicial:,.2f}")
            print(f"  Precio final:     ${precio_final:,.2f}")
            print(f"  Cambio:           {cambio_porcentual:+.2f}%")
            
            if cambio_porcentual > 0:
                print(f"  Tendencia:        ALCISTA ↑")
            elif cambio_porcentual < 0:
                print(f"  Tendencia:        BAJISTA ↓")
            else:
                print(f"  Tendencia:        NEUTRAL →")
            
            return {
                'precios': precios,
                'estadisticas': {
                    'minimo': precio_min,
                    'maximo': precio_max,
                    'promedio': precio_promedio,
                    'volatilidad': volatilidad,
                    'cambio_porcentual': cambio_porcentual
                }
            }
        
        except requests.exceptions.RequestException as e:
            print(f"\nError al obtener datos históricos: {e}")
            return None
    
    def comparar_criptomonedas(self):
        """Compara el rendimiento de múltiples criptomonedas"""
        print(f"\n\n{'='*60}")
        print("COMPARACIÓN DE RENDIMIENTO (24 horas)")
        print("="*60 + "\n")
        
        url = f"{self.base_url}/simple/price"
        params = {
            'ids': 'bitcoin,ethereum,cardano,solana,polkadot',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            datos = response.json()
            
            # Ordenar por cambio porcentual
            ranking = sorted(
                datos.items(),
                key=lambda x: x[1]['usd_24h_change'],
                reverse=True
            )
            
            print("Ranking por rendimiento:")
            print("-" * 40)
            
            for i, (crypto, info) in enumerate(ranking, 1):
                cambio = info['usd_24h_change']
                emoji = "🟢" if cambio > 0 else "🔴"
                print(f"{i}. {crypto.upper():12} {cambio:+7.2f}% {emoji}")
            
            return ranking
        
        except requests.exceptions.RequestException as e:
            print(f"\nError en comparación: {e}")
            return None

def main():
    """Función principal que ejecuta todos los análisis"""
    analyzer = CryptoAnalyzer()
    
    # 1. Obtener precios actuales
    precios_actuales = analyzer.obtener_precios_actuales()
    
    # 2. Obtener datos históricos de Bitcoin
    datos_historicos = analyzer.obtener_datos_historicos('bitcoin', dias=30)
    
    # 3. Comparar rendimiento
    comparacion = analyzer.comparar_criptomonedas()
    
    print("\n" + "="*60)
    print("ANÁLISIS COMPLETADO")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()