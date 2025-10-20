import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ProductoService, Producto, CryptoData, HistoricalData } from './producto.service';

interface EstadisticasCrypto {
  minimo: number;
  maximo: number;
  promedio: number;
  volatilidad: number;
  cambioTotal: number;
  tendencia: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  // CRUD
  productos: Producto[] = [];
  productoActual: Producto = {
    nombre: '',
    descripcion: '',
    precio: 0
  };
  editando = false;
  idEditando: number | null = null;

  // API Externa
  criptomonedas: CryptoData[] = [];
  cargandoCripto = false;
  
  // Análisis
  cryptoSeleccionada: string = 'bitcoin';
  diasAnalisis: number = 7;
  datosHistoricos: number[] = [];
  estadisticas: EstadisticasCrypto | null = null;
  analizando = false;

  constructor(private productoService: ProductoService) {}

  ngOnInit() {
    this.cargarProductos();
    this.cargarCriptomonedas();
  }

  // ==================== CRUD ====================
  cargarProductos() {
    this.productoService.listar().subscribe({
      next: (data) => this.productos = data,
      error: (err) => console.error('Error:', err)
    });
  }

  guardar() {
    if (this.editando && this.idEditando) {
      this.productoService.editar(this.idEditando, this.productoActual).subscribe({
        next: () => {
          alert('Producto actualizado exitosamente');
          this.cargarProductos();
          this.cancelar();
        },
        error: (err) => alert('Error al actualizar el producto')
      });
    } else {
      this.productoService.crear(this.productoActual).subscribe({
        next: () => {
          alert('Producto creado exitosamente');
          this.cargarProductos();
          this.cancelar();
        },
        error: (err) => alert('Error al crear el producto')
      });
    }
  }

  editar(producto: Producto) {
    this.editando = true;
    this.idEditando = producto.id!;
    this.productoActual = { ...producto };
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  eliminar(id: number) {
    if (confirm('¿Está seguro de eliminar este producto?')) {
      this.productoService.eliminar(id).subscribe({
        next: () => {
          alert('Producto eliminado exitosamente');
          this.cargarProductos();
        },
        error: (err) => alert('Error al eliminar el producto')
      });
    }
  }

  cancelar() {
    this.productoActual = { nombre: '', descripcion: '', precio: 0 };
    this.editando = false;
    this.idEditando = null;
  }

  // ==================== API EXTERNA ====================
  cargarCriptomonedas() {
    this.cargandoCripto = true;
    this.productoService.obtenerCriptomonedas().subscribe({
      next: (data) => {
        this.criptomonedas = data;
        this.cargandoCripto = false;
      },
      error: (err) => {
        console.error('Error al cargar criptomonedas:', err);
        this.cargandoCripto = false;
      }
    });
  }

  analizarCripto() {
    this.analizando = true;
    this.estadisticas = null;
    
    this.productoService.obtenerHistorico(this.cryptoSeleccionada, this.diasAnalisis).subscribe({
      next: (data: HistoricalData) => {
        // Extraer solo los precios
        this.datosHistoricos = data.prices.map(p => p[1]);
        
        // Calcular estadísticas
        this.calcularEstadisticas();
        this.analizando = false;
      },
      error: (err) => {
        console.error('Error al obtener histórico:', err);
        this.analizando = false;
        alert('Error al analizar los datos históricos');
      }
    });
  }

  calcularEstadisticas() {
    if (this.datosHistoricos.length === 0) return;

    const precios = this.datosHistoricos;
    const minimo = Math.min(...precios);
    const maximo = Math.max(...precios);
    const promedio = precios.reduce((a, b) => a + b, 0) / precios.length;
    const volatilidad = ((maximo - minimo) / promedio) * 100;
    
    const precioInicial = precios[0];
    const precioFinal = precios[precios.length - 1];
    const cambioTotal = ((precioFinal - precioInicial) / precioInicial) * 100;
    
    let tendencia = 'NEUTRAL';
    if (cambioTotal > 2) tendencia = 'ALCISTA';
    else if (cambioTotal < -2) tendencia = 'BAJISTA';

    this.estadisticas = {
      minimo,
      maximo,
      promedio,
      volatilidad,
      cambioTotal,
      tendencia
    };
  }

  getNombreCrypto(id: string): string {
    const nombres: any = {
      'bitcoin': 'Bitcoin',
      'ethereum': 'Ethereum',
      'cardano': 'Cardano',
      'solana': 'Solana',
      'polkadot': 'Polkadot'
    };
    return nombres[id] || id;
  }

  getTendenciaClass(tendencia: string): string {
    if (tendencia === 'ALCISTA') return 'alcista';
    if (tendencia === 'BAJISTA') return 'bajista';
    return 'neutral';
  }
}