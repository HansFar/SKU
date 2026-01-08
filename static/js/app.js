document.addEventListener("DOMContentLoaded", () => {
    cargarEstado();
});

let datosGlobales = [];

// =======================
// ESTADO DEL EXCEL
// =======================
function cargarEstado() {
    fetch("/estado")
        .then(res => res.json())
        .then(data => {
            document.getElementById("estado").textContent =
                data.archivo
                    ? "✔ Excel cargado: " + data.archivo
                    : "⚠ No hay Excel cargado";
        });
}

// =======================
// BUSCAR SKU
// =======================
function buscar() {
    const sku = document.getElementById("sku").value.trim();
    if (!sku) return;

    fetch("/buscar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sku })
    })
    .then(res => res.json())
    .then(data => {
        console.log("📦 Datos recibidos:", data);
        datosGlobales = data;
        poblarFiltroAreas(data);
        renderTabla(data);
        mostrarResumen(data, sku);
    });
}

// =======================
// ACTUALIZAR EXCEL
// =======================
function actualizar() {
    fetch("/actualizar", { method: "POST" })
        .then(() => {
            alert("Excel actualizado");
            cargarEstado();
        });
}

// =======================
// SUBIR ARCHIVO
// =======================

function subirExcel() {
    const input = document.getElementById("excelFile");
    if (!input.files.length) {
        alert("Seleccione un archivo Excel");
        return;
    }

    const formData = new FormData();
    formData.append("file", input.files[0]);

    fetch("/subir_excel", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        alert(data.mensaje);
        cargarEstado();
    });
}



// =======================
// RESUMEN SKU
// =======================
function mostrarResumen(data, sku) {
    const resumen = document.getElementById("resumen");

    if (!data || data.length === 0) {
        resumen.innerHTML = "<b>No se encontraron resultados</b>";
        return;
    }

    const descripcion = data[0].descripcion || "";

    resumen.innerHTML = `
        <strong>SKU:</strong> ${sku}<br>
        <strong>Descripción:</strong> ${descripcion}
    `;
}


// =======================
// FILTRO DE ÁREAS
// =======================
function poblarFiltroAreas(data) {
    const filtro = document.getElementById("filtroArea");
    filtro.innerHTML = `<option value="">Todas las áreas</option>`;

    const areas = [...new Set(data.map(f => f.area))];

    areas.forEach(a => {
        if (a) filtro.innerHTML += `<option value="${a}">${a}</option>`;
    });
}


function aplicarFiltros() {
    const area = document.getElementById("filtroArea").value;
    const filtrado = area
        ? datosGlobales.filter(f => f.area === area)
        : datosGlobales;

    renderTabla(filtrado);
}


// =======================
// TABLA (POR POSICIÓN)
// =======================
function renderTabla(data) {
    const tbody = document.querySelector("#tablaResultados tbody");
    const totalDiv = document.getElementById("totalStock");

    tbody.innerHTML = "";
    let total = 0;

    data.forEach(item => {
        const area        = item.area || "";
        const ubicacion   = item.ubicacion || "";
        const descripcion = item.descripcion || "";
        const stock       = Number(item.stock) || 0;
        const asignado    = Number(item.asignado) || 0;
        const bloqueado   = item.bloqueado || "";

        total += stock;

        tbody.innerHTML += `
            <tr class="${bloqueado ? 'bloqueado' : ''}">
                <td>${area}</td>
                <td>${ubicacion}</td>
                <td>${descripcion}</td>
                <td>${stock}</td>
                <td>${asignado}</td>
                <td>${bloqueado ? "SÍ" : "NO"}</td>
            </tr>
        `;
    });

    totalDiv.innerHTML = `<strong>Total stock:</strong> ${total}`;
}


