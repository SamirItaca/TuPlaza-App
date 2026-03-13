/**
 * Define la estructura de configuración de un botón dentro del componente de tabs.
 *
 * Esta interface se utiliza para describir cada pestaña de la navegación principal,
 * indicando la ruta asociada, el icono a mostrar y el texto visible para el usuario.
 */
export interface TabButtonPages {

  /**
   * Nombre o identificador de la pestaña.
   *
   * Generalmente coincide con el path de la ruta configurada en el router
   * (por ejemplo: 'home', 'garajes', 'favoritos').
   */
  tab: string;

  /**
   * Nombre del icono a mostrar en el botón de la pestaña.
   *
   * Debe corresponder con un icono válido de Ionicons
   * (por ejemplo: 'home-outline', 'heart', 'add-circle').
   */
  iconName: string;

  /**
   * Texto visible que se muestra debajo del icono en la pestaña.
   *
   * Es una etiqueta corta y descriptiva para el usuario final.
   */
  text: string;
}
