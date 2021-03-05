$(document).ready(function () {
    const email = $('#id_username')
    const url = '/check_email_authorization/'
    email.on('change', inputBlur)

    // Событие вызывается, когда происходит изменение Input.
    function inputBlur() {
        email.on('blur', checkEmail)
    }

    // Событие вызывается, когда указанный Input становиться не активным, меняет состояние.
    function checkEmail() {
        $.ajax({
            method: "GET",
            url: url,
            data: {
                'email': email.val()
            },
            dataType: 'json',
            success: function (data) {
                if (data.error_email) {
                    $('#errorEmail li').text(data.error_email)
                    $('.form-button').attr('disabled', true)
                } else {
                    $('#errorEmail li').text('')
                    $('.form-button').removeAttr('disabled')
                }
            }
        })
    }
})
