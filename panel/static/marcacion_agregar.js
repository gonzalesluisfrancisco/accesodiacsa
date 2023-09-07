function AgregarDatos() {
    console.log("Entra a agregardatos")
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
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    cardid = document.getElementById("cardid").value
    ubicacion = document.getElementById("ubicacion").value
    nombre = document.getElementById("nombre").value
    apellido = document.getElementById("apellido").value
    empresa = document.getElementById("empresa").value
    cargo = document.getElementById("cargo").value
    f_ingreso = document.getElementById("f_ingreso").value
    h_ingreso = document.getElementById("h_ingreso").value
    evento = document.getElementById("evento").value
    $.ajax({
        url: '',
        method: 'POST',
        data: {
            comando: "agregarLivedata",
            cardid: cardid,
            ubicacion: ubicacion,
            nombre: nombre,
            apellido: apellido,
            empresa: empresa,
            cargo: cargo,
            f_ingreso: f_ingreso,
            h_ingreso: h_ingreso,
            evento: evento,
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
                return
            }
            Swal.fire({
                icon: 'success',
                title: 'Correcto',
                text: response.Mensaje
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.reload()
                }
            });
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

function BusquedaDatos() {
    CardID = document.getElementById("cardid").value
    if (CardID.length != 8) return;
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
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log(CardID)
    $.ajax({
        url: '',
        method: 'POST',
        data: {
            Comando: "EliminarEntrada",
            cardid: CardID,
            csrfmiddlewaretoken: csrfToken,
            comando: "consultaDatos"
        },
        success: function (response) {
            Swal.close();
            if (response.Estado == "Invalido") {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: response.Mensaje
                });
                return
            }
            document.getElementById("ubicacion").value = response.ubicacion
            document.getElementById("nombre").value = response.nombre
            document.getElementById("apellido").value = response.apellido
            document.getElementById("empresa").value = response.empresa
            document.getElementById("cargo").value = response.cargo
            document.getElementById("f_ingreso").value = response.f_ingreso
            document.getElementById("h_ingreso").value = response.h_ingreso
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