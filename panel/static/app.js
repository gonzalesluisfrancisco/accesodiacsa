/*$(document).ready(function () {
    //ActualizarValores()
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
});*/
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
/* <script>
  // $(document).ready(function () {
  //   $('#Marcacion').DataTable({
  //     "order": [[0, "desc"]]  // Orden descendente en la primera columna
  //   });
  // });
</script> */
var tabla;
var searchValue
$(document).ready(function () {
    tabla = $('#Marcacion').DataTable({
        processing: true,
        serverSide: true,
        ajax: {
            url: '/marcacion',  // Ruta URL de tu vista Django
            type: "POST",
            data: function (d) {
                d.Comando = "TablaMarcacion"
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
    $('#Marcacion thead input').on('input', function () {
        searchValue = $(this).val();
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

function RegistrarUsuario() {
    Swal.fire({
        title: 'Cargando...',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        },
        showConfirmButton: false,
        showCancelButton: false,
        allowEscapeKey: false,
        allowEnterKey: false,
    });
    var Nombre = document.getElementsByName("nuevousuario")[0].value
    var PrimerApellido = document.getElementsByName("nuevousuario")[1].value
    var SegundoApellido = document.getElementsByName("nuevousuario")[2].value
    var DNI = document.getElementsByName("nuevousuario")[3].value
    var Correo = document.getElementsByName("nuevousuario")[4].value
    var Telefono = document.getElementsByName("nuevousuario")[5].value
    var Rol = document.getElementsByName("nuevousuario")[6].value
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: "POST",
        url: "",
        data: {
            csrfmiddlewaretoken: csrfToken,
            Comando: "RegistrarUsuario",
            Nombre: Nombre,
            PrimerApellido: PrimerApellido,
            SegundoApellido: SegundoApellido,
            DNI: DNI,
            Correo: Correo,
            Telefono: Telefono,
            Rol: Rol
        },
        success: function (response) {
            Swal.close();
            if (response.Estado == "Invalido") {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: response.Mensaje
                });
            }
            else {
                Swal.fire({
                    icon: 'success',
                    title: 'Correcto',
                    text: response.Mensaje
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location.reload();
                    }
                });
            }
            return response;
        },
        error: function (xhr, status, error) {
            Swal.close();
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: error
            });
        }
    });
}

function EnviarExcel(Comando, index) {
    Swal.fire({
        title: 'Cargando...',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        },
        showConfirmButton: false,
        showCancelButton: false,
        allowEscapeKey: false,
        allowEnterKey: false,
    });
    var fileInput = document.getElementsByName('excelFile')[index - 1];
    var file = fileInput.files[0];
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log(Comando)
    if (file) {
        var formData = new FormData();
        formData.append('excelFile', file);
        $.ajax({
            type: 'POST',
            url: '',
            data: formData,
            contentType: false,
            processData: false,
            headers: {
                'X-CSRFToken': csrfToken,
            },
            success: function (response) {
                Swal.close();
                if (response.Estado == "Invalido") {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: response.Mensaje
                    });
                }
                else {
                    Swal.fire({
                        icon: 'success',
                        title: 'Correcto',
                        text: response.Mensaje
                    });
                }
                return response;
            },
            error: function (xhr, status, error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error
                });
            }
        });
    }
}

function ActualizarValores() {
    Swal.fire({
        title: 'Cargando...',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        },
        showConfirmButton: false,
        showCancelButton: false,
        allowEscapeKey: false,
        allowEnterKey: false,
    });
    var Usuario = $("#usuario").val();
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: "POST",
        url: "",
        data: {
            Comando: "ConsultarDatos",
            Usuario: Usuario,
            csrfmiddlewaretoken: csrfToken,
        },
        success: function (response) {
            Swal.close();
            if (response.Estado == "Invalido") {
                document.getElementsByName("nuevousuario")[0].placeholder = "No hay datos"
                document.getElementsByName("nuevousuario")[1].placeholder = "No hay datos"
                document.getElementsByName("nuevousuario")[2].placeholder = "No hay datos"
                document.getElementsByName("nuevousuario")[3].placeholder = "No hay datos"
                document.getElementsByName("nuevousuario")[4].placeholder = "No hay datos"
                document.getElementsByName("nuevousuario")[5].placeholder = "No hay datos"
                document.getElementsByName("nuevousuario")[6].placeholder = "No hay datos"
            }
            else {
                document.getElementsByName("nuevousuario")[0].placeholder = response.Nombre
                document.getElementsByName("nuevousuario")[1].placeholder = response.PrimerApellido
                document.getElementsByName("nuevousuario")[2].placeholder = response.SegundoApellido
                document.getElementsByName("nuevousuario")[3].placeholder = response.DNI
                document.getElementsByName("nuevousuario")[4].placeholder = response.Correo
                document.getElementsByName("nuevousuario")[5].placeholder = response.Telefono
                document.getElementsByName("nuevousuario")[6].placeholder = response.Rol
            }
            return
        },
        error: function (xhr, status, error) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: error
            });
        }
    });
}

function EliminarUsuario() {
    Swal.fire({
        title: 'Cargando...',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        },
        showConfirmButton: false,
        showCancelButton: false,
        allowEscapeKey: false,
        allowEnterKey: false,
    });
    var Usuario = $("#usuario").val();
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: "POST",
        url: "",
        data: {
            Comando: "EliminarUsuario",
            Usuario: Usuario,
            csrfmiddlewaretoken: csrfToken,
        },
        success: function (response) {
            Swal.close();
            if (response.Estado == "Invalido") {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: response.Mensaje
                });
            }
            else {
                Swal.fire({
                    icon: 'success',
                    title: 'Correcto',
                    text: response.Mensaje
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location.reload();
                    }
                });
            }
            return
        },
        error: function (xhr, status, error) {
            Swal.close();
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: error
            });
        }
    });
}

function DescargarExcel() {
    Swal.fire({
        title: 'Cargando...',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        },
        showConfirmButton: false,
        showCancelButton: false,
        allowEscapeKey: false,
        allowEnterKey: false,
    });

    var searchValue = '';


    $.ajax({
        url: '',
        method: 'GET',
        data: {
            Comando: "DescargarExcel",
            FechaInicial: $('#min').val(),
            FechaFinal: $('#max').val(),
            Search: document.getElementsByClassName("form-control form-control-sm")[0].value,
        },
        xhrFields: {
            responseType: 'blob'
        },
        success: function (data) {
            Swal.close()
            var a = document.createElement('a');
            var url = window.URL.createObjectURL(data);
            a.href = url;
            a.download = 'Historial_ingresos_salidas.xlsx';
            a.click();
            window.URL.revokeObjectURL(url);
        },
        error: function (xhr, status, error) {
            Swal.close();
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: error
            });
        }
    });

}