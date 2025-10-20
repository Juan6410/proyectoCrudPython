import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ProductoService, Producto } from './producto.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  productos: Producto[] = [];
  
  productoActual: Producto = {
    nombre: '',
    descripcion: '',
    precio: 0
  };
  
  editando = false;
  idEditando: number | null = null;

  constructor(private productoService: ProductoService) {}

  ngOnInit() {
    this.cargarProductos();
  }

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
          alert('✅ Producto actualizado');
          this.cargarProductos();
          this.cancelar();
        },
        error: (err) => alert('❌ Error al actualizar')
      });
    } else {
      this.productoService.crear(this.productoActual).subscribe({
        next: () => {
          alert('✅ Producto creado');
          this.cargarProductos();
          this.cancelar();
        },
        error: (err) => alert('❌ Error al crear')
      });
    }
  }

  editar(producto: Producto) {
    this.editando = true;
    this.idEditando = producto.id!;
    this.productoActual = { ...producto };
  }

  eliminar(id: number) {
    if (confirm('¿Eliminar este producto?')) {
      this.productoService.eliminar(id).subscribe({
        next: () => {
          alert('✅ Producto eliminado');
          this.cargarProductos();
        },
        error: (err) => alert('❌ Error al eliminar')
      });
    }
  }

  cancelar() {
    this.productoActual = { nombre: '', descripcion: '', precio: 0 };
    this.editando = false;
    this.idEditando = null;
  }
}