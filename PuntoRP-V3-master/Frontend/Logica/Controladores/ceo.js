
function toggleDropdown() {
            const lista = document.getElementById("listaEliminar");
            lista.style.display = lista.style.display === "none" || lista.style.display === "" ? "block" : "none";
        }

// Botón para cargar el formulario de agregar membresías
document.getElementById('cargar_membresias_form').addEventListener('click', function () {
    const formHTML = `
        <form id="membresias_form" style="color:white;">
            <label for="nombre">Nombre:</label>
            <input type="text" id="nombre" name="nombre" required>
            <label for="precio">Precio:</label>
            <input type="number" id="precio" name="precio" required>
            <label for="detalles">Detalle:</label>
            <input type="text" id="detalles" name="detalles" required>            
            <button type="submit">Agregar Membresías</button>
        </form>
    `;
    document.getElementById('contenedorFormulario').innerHTML = formHTML;

    document.getElementById('membresias_form').addEventListener('submit', async function (event) {
        event.preventDefault();

        const response = await fetch("http://127.0.0.1:5000/crear_membresia", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nombre: document.getElementById('nombre').value,
                precio: document.getElementById('precio').value,
                detalles: document.getElementById('detalles').value
            })
        });

        if (response.ok) {
            alert('Membresía agregada con éxito');
            document.getElementById('contenedorFormulario').innerHTML = '';
        } else {
            alert('Error al agregar la membresía');
        }
    });
});


// Botón para cargar la lista de membresías a eliminar
document.getElementById('eliminar_membresias_form').addEventListener('click', async function (event) {
    event.preventDefault();
    const contenedor = document.getElementById('contenedorFormulario');

    const response = await fetch("http://127.0.0.1:5000/get_all_membresias", {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });

    if (!response.ok) {
        alert('Error al obtener membresías');
        return;
    }

    const membresias = await response.json();
    contenedor.innerHTML = '';

    membresias.forEach(element => {
        const div = document.createElement("div");
        div.innerHTML = `
            <div style="width:100%;height:100%;margin:auto;background-color:grey;border:white 1px solid;border-radius:5px;display:flex;flex-direction:column;color:white;justify-content:center;align-items:center;">
                <span>Nombre: ${element.nombre}</span>
                <span>Precio: ${element.precio}</span>
                <span>Detalles: ${element.detalles}</span>
                <label>
                    <button class="checkbox-membresia" data-nombre="${element.nombre}"> Eliminar </button>
                </label>
            </div>`;
        contenedor.appendChild(div);
    });
});


// Delegación de eventos para los checkboxes que eliminan membresías
document.getElementById('contenedorFormulario').addEventListener('click', async function (event) {

        try {
            const response = await fetch("http://127.0.0.1:5000/eliminar_membresia", {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nombre: nombre })
            });

            const data = await response.json();

            if (!data.ok) {
                console.log(data);
                throw new Error('Error al eliminar');
            }

            alert('¡Membresía eliminada con éxito!');
            // Eliminar el div del DOM
            event.target.closest("div").remove();

        } catch (error) {
            alert('Ocurrió un error: ' + error.message);
        }
    });
