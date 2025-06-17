document.getElementById('cargar_vehiculos_form').addEventListener('click',async function(event){
event.preventDefault()

    contenedor = document.getElementById('contenedorFormulario');
    contenedor.innerHTML = "";

    const formHTML = `<form id="vehiculos_form" style="color:white;">
                <label for="nombre">Nombre:</label>
                <input type="text" id="nombre" name="nombre" required>
                <label for="precio">Precio:</label>
                <input type="number" id="precio" name="precio" required>
                <label for="detalle">Detalles</label>
                <input type="text" id="detalle" name="detalle" required>            
                <button type="submit">Agregar Vehiculo</button>
            </form>`
    contenedor.innerHTML = formHTML

    document.getElementById('vehiculos_form').addEventListener('submit',async function(event){
    event.preventDefault()
        const nombre = document.getElementById('nombre').value;
        const precio = document.getElementById('precio').value;
        const detalle = document.getElementById('detalle').value;
        console.log("Datos a enviar:", { nombre, precio, detalle });
    const response = await fetch("http://127.0.0.1:5000/crear_vehiculo", {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                                nombre,
                                precio,
                                detalle
                            })})
const data = await response.json();
    if (!response.ok){
        throw new Error("error al obtener response de la Api",data)
    }
    else{
        return console.log('el error es ',data)
    }
})})