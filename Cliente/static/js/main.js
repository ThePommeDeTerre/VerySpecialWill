// Controlador do index
const IndexHelper = function () {

    const isEmail = function(email)
    {
        var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        return regex.test(email);
    }

    //Funcao para ajudar a ver se está vazio (because javascript)
    const isEmpty = function (value) {
        return typeof value == 'string' && !value.trim() || typeof value == 'undefined' || value === null;
    }

    // Mete o atual csrf sempre que é efetuada uma chamada ajax
    const setupAjax = () => {
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                const csrf = $('#csrf_token').val();
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf);
                }
            }
        });
    }

    const handleAjaxError = (data) => {
        const divMessages = $('#alert-messages');
        divMessages.html('')

        let message = data.msg ? data.msg : ''

        let errorDiv = $('<div>')
        errorDiv.addClass('toast toast-error').text(message)
        divMessages.append(errorDiv)

    }

    const init = () => {
        initTab()
        initForm()
        setupAjax()
    }

    //#region formulário
    //Inicializa o formulário, botões e ações
    const initForm = () => {
        $('#btn-login').on('click', login);
        $('#btn-registo').on('click', registo);
    }

    const login = function () {
        // Seleciona o botão pressionado e faz disable (impedir multiple requests)
        let btnElement = $(this);
        btnElement.attr('disabled', true)

        const user = $('#input-login-username').val();
        const pass = $('#input-login-password').val();

        //Verifica se os campos estao a vazio
        if (isEmpty(user) || isEmpty(pass)) {
            return alert('Por favor preencha todos os campos');
        }

        //manda o request para o login
        $.ajax({
                type: "POST",
                url: 'login',
                data: JSON.stringify({username: user, password: pass}),
                success: (data, status) => {
                    // Retira o disabled
                    btnElement.attr('disabled', false)
                    if (!data.success)
                        handleAjaxError(data)
                    else
                        alert('nice')
                },
                error: (data) => {
                    // Retira o disabled
                    btnElement.attr('disabled', false)
                    handleAjaxError(data.responseJSON)
                },
                contentType: "application/json",
                dataType: 'json'

            }
        )
    }

    const registo = function () {
        // Seleciona o botão pressionado e faz disable (impedir multiple requests)
        let btnElement = $(this);
        btnElement.attr('disabled', true)

        const user = $('#input-registo-username').val();
        const pass = $('#input-registo-password').val();
        const email = $('#input-registo-email').val();

        //Verifica se os campos estao a vazio
        if (isEmpty(user) || isEmpty(pass) || isEmpty(email)) {
            return alert('Por favor preencha todos os campos');
        }

        if(!isEmail(email)){
            return alert('Email inválido');
        }

        //manda o request para o registo
        $.ajax({
                type: "POST",
                url: 'registo',
                data: JSON.stringify({username: user, password: pass, email: email}),
                success: (data, status, xhttp) => {
                    // Retira o disabled
                    btnElement.attr('disabled', false)

                    if (!data.success)
                        handleAjaxError(data)
                    else
                        alert('nice')
                },
                error: (data) => {
                    // Retira o disabled
                    btnElement.attr('disabled', false)
                    handleAjaxError(data.responseJSON)
                },
                contentType: "application/json",
                dataType: 'json'

            }
        )
    }

//#endregion

//#region mudar as tabs
    const initTab = () => {
        let tabs = $('.tab-item')
        $.each(tabs, (i, v) => {
            $(v).on('click', function () {
                const tabName = $($(this).find('a')[0]).data('tab')
                changeTab(this, tabName)
                $(this).addClass('active')
            })
        })
    }

    const changeTab = (v, tabName) => {
        $('.tab-content').hide()
        $('.tab-item').removeClass('active')
        $('#' + tabName).show()
        $(this).addClass('active')
    }
//#endregion

    return {
        init: init
    }
}
();

$(function () {
    IndexHelper.init()
})