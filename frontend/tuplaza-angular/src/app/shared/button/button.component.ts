import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

type ButtonType = 'primary' | 'secundary';
type ButtonSize = 'sm' | 'md' | 'lg'

/**
 * Componente de botón reutilizable de TuPlaza.
 *
 * Este componente permite renderizar botones con estilos predefinidos según tipo
 * y tamaño. Se puede configurar como habilitado o deshabilitado.
 *
 * @example
 * ```html
 * <tuplaza-button
 *   text="Comprar ahora"
 *   type="primary"
 *   size="lg"
 *   [isDisabled]="false">
 * </tuplaza-button>
 * ```
 */
@Component({
  selector: 'tuplaza-button',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './button.component.html',
  styleUrl: './button.component.css'
})
export class ButtonComponent {
  
  /**
   * Texto que se mostrará dentro del botón.
   * @required
   * @default ''
   */
  @Input() text: string = '';

  /**
   * Define el estilo del botón.
   * - `primary`: Botón principal con estilo destacado.
   * - `secundary`: Botón secundario con estilo neutro.
   * @default 'primary'
   */
  @Input() type: ButtonType = 'primary';

  /**
   * Tamaño del botón.
   * - `sm`: Botón pequeño.
   * - `md`: Tamaño mediano.
   * - `lg`: Botón grande.
   * @default 'md'
   */
  @Input() size: ButtonSize = 'md';

  /**
   * Indica si el botón está deshabilitado.
   * Si es `true`, el botón no será clickeable.
   * @default false
   */
  @Input() isDisabled: boolean = false;

  /** Prefijo base para las clases CSS del botón. */
  private baseCss: string = 'tuplaza-btn-';

  /** Estilos CSS según el tipo de botón. */
  CLASS_BY_TYPE: Record<ButtonType, string> = {
    primary: this.baseCss + 'primary',
    secundary: this.baseCss + 'secundary',
  } as const;

  /** Estilos CSS según el tamaño del botón. */
  CLASS_BY_SIZE: Record<ButtonSize, string> = {
    sm: this.baseCss + 'sm',
    md: this.baseCss + 'md',
    lg: this.baseCss + 'lg'
  } as const;

}
