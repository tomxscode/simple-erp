// VALORES FIJOS
// Obtener la URL del sitio
const SITIO = "http://127.0.0.1:5000";

// Obtenemos los elementos de interés
const burger = document.querySelector('.navbar-burger');
const menu = document.querySelector('.navbar-menu');

// Escuchamos el click sobre el navbar-burger
burger.addEventListener('click', () => {

  // Alternamos la clase is-active sobre ambos
  burger.classList.toggle('is-active');
  menu.classList.toggle('is-active');

});