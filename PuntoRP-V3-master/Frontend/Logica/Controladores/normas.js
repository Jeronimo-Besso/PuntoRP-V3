
export function renderizarNormasLogic() {
    const normas = {
        generales: "<h2>Normas Generales</h2><p>Lorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem</p>",
        same: "<h2>Normas Same</h2><p>Estas son las normas del SAME...</p>",
        pfa: "<h2>Normas PFA</h2><p>Normas de la Policía Federal Argentina...</p>",
        mafias: "<h2>Normas Mafias</h2><p>Normas internas de las mafias en el server...</p>",
    };

    const botones = document.querySelectorAll(".contenedor-normativas button");
    const contenedorInfo = document.querySelector(".info-normativas-data");

    if (botones.length && contenedorInfo) {
        botones.forEach(btn => {
            btn.addEventListener("click", () => {
                const area = btn.getAttribute("data-area");
                contenedorInfo.innerHTML = normas[area];
            });
        });

        // Mostrar por defecto las normas generales
        contenedorInfo.innerHTML = normas["generales"];
    }
}
