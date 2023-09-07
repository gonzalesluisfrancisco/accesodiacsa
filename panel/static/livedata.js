setInterval(function () {
    updateData();
}, 10000);

function updateData() {
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: "POST",
        url: "",
        data: {
            csrfmiddlewaretoken: csrfToken,
            Comando: "ObtenerHoraTotal",
        },
        success: function (response) {
            if (response.Estado == "Valido") {
                document.getElementById("total").innerHTML = response.Total
                document.getElementById("ultimaactualizacion").innerHTML = response.Hora
                tabla2.ajax.reload(null, false);
            }
        },
        error: function (xhr, status, error) {
            return
        }
    });
}

var tabla2;
$(document).ready(function () {
    tabla2 = $('#DataLive').DataTable({
        processing: true,
        serverSide: true,
        ajax: {
            url: '',  // Ruta URL de tu vista Django
            type: "POST",
            data: function (d) {
                d.Comando = "TablaLiveData"
                d.csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();
            },
        },
        "order": [[0, "asc"]],
        columns: [
            { data: "id" },
            { data: "ubicacion" },
            { data: "cardidHex" },
            { data: "nombre" },
            { data: "apellido" },
            { data: "empresa" },
            { data: "cargo" },
            { data: "f_evento" },
            { data: "h_evento" },
        ],
    });
});