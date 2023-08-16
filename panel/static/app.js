$(document).ready(function () {
    $('#DataLive').DataTable({
        language: {
            search: "Buscar:",
            lengthMenu: "Mostrar _MENU_ registros",
            info: "Mostrando del _START_ al _END_ de _TOTAL_ registros",
            infoEmpty: "No hay registros disponibles",
            infoFiltered: "(filtrado de _MAX_ registros totales)",
            paginate: {
                first: "Primero",
                last: "Último",
                next: "Siguiente",
                previous: "Anterior"
            }
        }
    });
});
/* <script>
  // $(document).ready(function () {
  //   $('#Marcacion').DataTable({
  //     "order": [[0, "desc"]]  // Orden descendente en la primera columna
  //   });
  // });
</script> */
var tabla;
$(document).ready(function () {
    tabla = $('#Marcacion').DataTable({
        processing: true,
        serverSide: true,
        ajax: {
            url: '/marcacion',  // Ruta URL de tu vista Django
            type: "POST",
            data: function (d) {
                d.min = $('#min').val();
                d.max = $('#max').val();
                d.csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();
            },
        },
        "order": [[0, "desc"]],
        columns: [
            { data: "id" },
            { data: "ubicacion" },
            { data: "cardidHex" },
            { data: "nombre" },
            { data: "apellido" },
            { data: "cargo" },
            { data: "f_evento" },
            { data: "h_evento" },
            { data: "evento" },
        ],
    });
});


$(document).ready(function () {
    $('#NoRegistrados').DataTable({
        language: {
            search: "Buscar:",
            lengthMenu: "Mostrar _MENU_ registros",
            info: "Mostrando del _START_ al _END_ de _TOTAL_ registros",
            infoEmpty: "No hay registros disponibles",
            infoFiltered: "(filtrado de _MAX_ registros totales)",
            paginate: {
                first: "Primero",
                last: "Último",
                next: "Siguiente",
                previous: "Anterior"
            }
        }
    });
});