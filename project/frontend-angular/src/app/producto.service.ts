import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Producto {
  id?: number;
  nombre: string;
  descripcion: string;
  precio: number;
}

export interface CryptoData {
  id: string;
  symbol: string;
  name: string;
  current_price: number;
  price_change_percentage_24h: number;
  market_cap: number;
  total_volume: number;
  high_24h: number;
  low_24h: number;
}

export interface HistoricalData {
  prices: number[][];
  market_caps: number[][];
  total_volumes: number[][];
}

@Injectable({
  providedIn: 'root'
})
export class ProductoService {
  private API_URL = 'http://localhost:8000/productos';
  private CRYPTO_API = 'https://api.coingecko.com/api/v3';

  constructor(private http: HttpClient) {}

  // CRUD Productos
  listar(): Observable<Producto[]> {
    return this.http.get<Producto[]>(this.API_URL);
  }

  crear(producto: Producto): Observable<any> {
    return this.http.post(this.API_URL, producto);
  }

  editar(id: number, producto: Producto): Observable<any> {
    return this.http.put(`${this.API_URL}/${id}`, producto);
  }

  eliminar(id: number): Observable<any> {
    return this.http.delete(`${this.API_URL}/${id}`);
  }

  // API Externa - CoinGecko
  obtenerCriptomonedas(): Observable<CryptoData[]> {
    const url = `${this.CRYPTO_API}/coins/markets`;
    const params = {
      vs_currency: 'usd',
      ids: 'bitcoin,ethereum,cardano,solana,polkadot',
      order: 'market_cap_desc'
    };
    return this.http.get<CryptoData[]>(url, { params });
  }

  obtenerHistorico(cryptoId: string, days: number): Observable<HistoricalData> {
    const url = `${this.CRYPTO_API}/coins/${cryptoId}/market_chart`;
    const params = {
      vs_currency: 'usd',
      days: days.toString()
    };
    return this.http.get<HistoricalData>(url, { params });
  }
}