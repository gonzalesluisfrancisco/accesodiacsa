var DEBUG = true
document.addEventListener("DOMContentLoaded", function () {
    $("[name='PantallaLogin']").css("display", "flex");
    $("[name='PantallaToken']").css("display", "none");
    $("[name='PantallaContrasenaOlvidada']").css("display", "none");
});
function EnviarCredenciales() {
    var Usuario = $("#username").val()
    var Contrasena = $("#password").val()
    var Captcha = VerificarCaptcha()
    if (!DatosIngresadosValidos(Usuario, Contrasena, Captcha)) return;
    if (DEBUG) console.log(`Usuario: ${Usuario}\nContraseña: ${Contrasena}\nCaptcha: ${Captcha}`)
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $(".loader").css("display", "flex")
    $.ajax({
        type: "POST",
        url: "/",
        data: {
            csrfmiddlewaretoken: csrfToken,
            Comando: "VerificarLogin",
            Usuario: Usuario,
            Contrasena: Contrasena,
            Captcha: Captcha
        },
        success: function (response) {
            if (DEBUG) console.log(response.Mensaje)
            $(".loader").css("display", "none")
            if (response.Mensaje == "El usuario y contraseña son correctos") MostarSegundoFactor();
            else alert(response.Mensaje)
            return response;
        },
        error: function (xhr, status, error) {
            $(".loader").css("display", "none")
            alert(error);
        }
    });

}

function VerificarCaptcha() {
    var recaptchaResponse = grecaptcha.getResponse();
    if (recaptchaResponse === "") {
        return "Fallido";
    } else {
        return recaptchaResponse;
        ;
    }
}

function DatosIngresadosValidos(Usuario, Password, CAPTCHA) {
    if (DEBUG) return true;
    if (Usuario.length < 6) { alert("El usuario debe tener 6 caracteres como mínimo."); return false; }
    if (Password.length < 6) { alert("El password debe tener 8 caracteres como mínimo."); return false; }
    if (CAPTCHA.length < 10) { alert("Debe validar el CAPTCHA para continuar"); return false; }
    return true;
}

function MostarSegundoFactor() {
    $("[name='PantallaLogin']").css("display", "none");
    $("[name='PantallaToken']").css("display", "flex");
    $("[name='PantallaContrasenaOlvidada']").css("display", "none");
}

function EnviarToken() {
    var Usuario = $("#username").val()
    var Contrasena = $("#password").val()
    var Captcha = VerificarCaptcha()
    var Token = $("#token").val()
    if (Token.length != 8) { alert("El token debe tener 8 caracteres"); return; }
    if (DEBUG) console.log(`Token: ${Token}`)
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $(".loader").css("display", "flex")
    $.ajax({
        type: "POST",
        url: "/",
        data: {
            csrfmiddlewaretoken: csrfToken,
            Comando: "VerificarToken",
            Usuario: Usuario,
            Contrasena: Contrasena,
            Captcha: Captcha,
            Token: Token
        },
        success: function (response) {
            if (DEBUG) console.log(response.Mensaje)
            $(".loader").css("display", "none")
            if (response.Mensaje == undefined) window.location.href = "/livedata";
            else alert(response.Mensaje)
            return response;
        },
        error: function (xhr, status, error) {
            $(".loader").css("display", "none")
            alert(error);
        }
    });
}

function MostrarContrasenaOlvidada() {
    $("[name='PantallaLogin']").css("display", "none");
    $("[name='PantallaToken']").css("display", "none");
    $("[name='PantallaContrasenaOlvidada']").css("display", "flex");
}

function EnviarContrasenaOlvidada() {
    var Correo = $("#correo").val()
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $(".loader").css("display", "flex")
    $.ajax({
        type: "POST",
        url: "/",
        data: {
            csrfmiddlewaretoken: csrfToken,
            Comando: "RecuperarCuenta",
            Correo: Correo,
        },
        success: function (response) {
            if (DEBUG) console.log(response.Mensaje)
            $(".loader").css("display", "none")
            if (response.Mensaje == "Credenciales enviadas") { alert.Mensaje; window.location.href = "/" }
            else alert(response.Mensaje)
            return response;
        },
        error: function (xhr, status, error) {
            $(".loader").css("display", "none")
            alert(error);
        }
    });
}