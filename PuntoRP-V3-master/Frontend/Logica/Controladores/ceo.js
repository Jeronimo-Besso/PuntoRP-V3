
function toggleDropdown() {
            const lista = document.getElementById("listaEliminar");
            lista.style.display = lista.style.display === "none" || lista.style.display === "" ? "block" : "none";
        }

document.getElementById('cargar_membresias_form').addEventListener('click', function() {
    const formHTML = `
        <form id="membresias_form" style="color:white;">
            <label for="nombre">Nombre:</label>
            <input type="text" id="nombre" name="nombre" required>
            <label for="precio">Precio:</label>
            <input type="number" id="precio" name="precio" required>
            <label for="detalles">Detalle</label>
            <input type="text" id="detalles" name="detalles" required>            
            <button type="submit">Agregar Membresias</button>
        </form>
    `;
    document.getElementById('contenedorFormulario').innerHTML = formHTML;

    document.getElementById('membresias_form').addEventListener('submit', async function(event) {
        event.preventDefault();

        const response = await fetch("http://127.0.0.1:5000/crear_membresia", {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                nombre: document.getElementById('nombre').value,
                precio: document.getElementById('precio').value,
                detalles:document.getElementById('detalles').value
            })
        });

            if(response.ok){
                alert('Membresia agregada con éxito');
                document.getElementById('contenedorFormulario').innerHTML = '';
            } else {
                alert('Error al agregar Membresia');
        }
    });
});

document.getElementById('eliminar_membresias_form').addEventListener('click',async function(event){
    event.preventDefault();
    const contenedor = document.getElementById('contenedorFormulario')
    const response = await fetch("http://127.0.0.1:5000/get_all_membresias", {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    }); //hacemos un fetch al endpoint, le aclaramos el metodo y el header para que vea de que es la peticio
    if (!response.ok){
        throw new Error('error al obtener membresias, response not ok')
    }
    contenedor.innerHTML = '';
    const membresias = await response.json()
    membresias.forEach(element => {
        const div = document.createElement("div");
        div.innerHTML = `<div style="width:100%;height:100%;margin:auto;background-color:grey;border:white 1px solid;border-radius:5px;display:flex;flex-direction:column;color:white;justify-content:center;align-items:center;"><span>Nombre: ${element.nombre}</span><span>Precio: ${element.precio}</span><span>Detalles: ${element.detalles}</span></div>`
        contenedor.appendChild(div);
 
    });

})
