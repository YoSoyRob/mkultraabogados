document.getElementById("legal-form").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    const datos = {
        actor: document.getElementById("actor").value,
        demandado: document.getElementById("demandado").value,
        documento_base: document.getElementById("documento_base").value,
        otras_pruebas: document.getElementById("otras_pruebas").value
    };
    
    const respuesta = await fetch("http://127.0.0.1:5000/generar_documento", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(datos)
    });
    
    const resultado = await respuesta.json();
    document.getElementById("mensaje").textContent = resultado.mensaje;
    
    if (resultado.archivo) {
        const enlace = document.createElement("a");
        enlace.href = `http://127.0.0.1:5000/${resultado.archivo}`;
        enlace.textContent = "Descargar Documento";
        enlace.setAttribute("download", resultado.archivo);
        document.body.appendChild(enlace);
    }
});