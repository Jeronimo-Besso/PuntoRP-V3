// tienda.js
export function renderizarTiendaLogic() {
  // Esperar a que el contenedor-productos exista en el DOM (porque recién insertaron tiendaHTML)
  const contenedorProductos = document.getElementById('contenedor-productos');
    document.getElementById("membresias").addEventListener('click',async function(e){
        contenedorProductos.innerHTML = ''
        const response = await fetch("http://127.0.0.1:5000/get_all_membresias", {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            return alert('Error al obtener membresías');
        }
        const membresias = await response.json();
        membresias.forEach(element => {
        const div = document.createElement("div");
        div.innerHTML = `
            <div class="container">
  <p class="title">${element.nombre}</p>
  <p class="price">$${element.precio}<span></span></p>
  <p class="description">${element.detalles}</p>
  <b class="offer">Actua rapido! Precios especiales inauguracion</b>
  <a class="subscribe-button" href="#">Comprar</a>
  <div class="ribbon-wrap">
    <div class="ribbon">Oferta Especial!</div>
  </div>
</div>`;
        contenedorProductos.appendChild(div);})})
////////////////////////////////////////////////////////////////////////////////  

    document.getElementById("mafias").addEventListener('click',async function(e){
        contenedorProductos.innerHTML = ''
        const response = await fetch("http://127.0.0.1:5000/get_all_mafias", {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            return alert('Error al obtener mafias');
        }
        const mafias = await response.json();
        mafias.forEach(element => {
        const div = document.createElement("div");
        div.innerHTML = `
            <div class="container">
  <p class="title">${element.nombre}</p>
  <p class="price">$${element.precio}<span></span></p>
  <p class="description">${element.detalles}</p>
  <a class="subscribe-button" href="#">Comprar</a>
</div>`;

        contenedorProductos.appendChild(div);})})


    document.getElementById("vehiculos").addEventListener('click',async function(e){
        contenedorProductos.innerHTML = ''
        const response = await fetch("http://127.0.0.1:5000/get_all_vehiculos", {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            return alert('Error al obtener vehiculos');
        }
        const mafias = await response.json();
        mafias.forEach(element => {
        const div = document.createElement("div");
        div.innerHTML = `
            <div class="card">
  <div class="image_container">
    <img src="/static/imgs/${element.vehiculo_img}" alt="${element.nombre}" class="image" />
  </div>
  <div class="title">
    <span>${element.nombre}</span>
    <br>
    <span>$${element.precio}</span>
    <br>
    <span>${element.detalles}</span>
  </div>
  <button class="cart-button">Comprar</button>
</div>
`;
        contenedorProductos.appendChild(div);})})



document.getElementById("coins").addEventListener('click',async function(e){
        contenedorProductos.innerHTML = ''
        const response = await fetch("http://127.0.0.1:5000/get_all_coins", {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            return alert('Error al obtener coins');
        }
        const coins = await response.json();
        coins.forEach(element => {
        const div = document.createElement("div");
        div.innerHTML = `
            <div class="container">
  <p class="title">${element.cantidad} Coins</p>
  <p class="price">$${element.precio}<span></span></p>
  <a class="subscribe-button" href="#">Comprar</a>
</div>`;

        contenedorProductos.appendChild(div);})})




























}
