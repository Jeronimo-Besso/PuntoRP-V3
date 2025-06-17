const palabras = [
    "Comunidad",
    "Familia",
    "Risas",
    "Amigos"
];

const texto = document.getElementById("palabra-dinamica");
let palabraIndex = 0;
let letraIndex = 0;
let borrando = false;

function escribir() {
    const palabra = palabras[palabraIndex];

    if (!borrando) {
        texto.textContent = palabra.slice(0, letraIndex++);
        if (letraIndex > palabra.length) {
            borrando = true;
            setTimeout(escribir, 1000); // Espera antes de borrar
            return;
        }
    } else {
        texto.textContent = palabra.slice(0, letraIndex--);
        if (letraIndex < 0) {
            palabraIndex = (palabraIndex + 1) % palabras.length;
            borrando = false;
            letraIndex = 0;
            setTimeout(escribir, 200); // Pausa antes de volver a escribir
            return;
        }
    }

    setTimeout(escribir, borrando ? 50 : 100);
}

// Iniciar animación al cargar
document.addEventListener("DOMContentLoaded", escribir);
