import { normasHTML } from '../templates/normasTemplate.js';
import { tiendaHTML } from '../templates/tiendaTemplate.js';
import { mainHTML } from '../templates/mainTemplate..js';
import { renderizarNormasLogic } from './normas.js';
import { renderizarTiendaLogic } from './tienda.js';

const contenedor = document.getElementById("contenedor");
contenedor.innerHTML = mainHTML
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("normas").addEventListener("click", (e) => {
        e.preventDefault();
        contenedor.innerHTML = normasHTML;
        renderizarNormasLogic();
    });

    document.getElementById("tienda").addEventListener("click", (e) => {
        e.preventDefault();
        contenedor.innerHTML = tiendaHTML;
        renderizarTiendaLogic();
    });

    document.getElementById("inicio").addEventListener("click",function(e){
        e.preventDefault();
        contenedor.innerHTML = mainHTML

    })
});

fetch('/api/session')
  .then(res => res.json())
  .then(data => {
    if(data.logged_in) {
      // Está logueado, redirigir a panel.html
      window.location.href = '../templates/panel.html'; 
    } else {
      // No está logueado, redirigir a login o mostrar mensaje
      window.location.href = '/Frontend/login.html';
    }
  });

