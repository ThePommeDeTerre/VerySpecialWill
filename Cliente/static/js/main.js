// Controlador do index
const IndexHelper = function () {

    //Funcao para ajudar a ver se está vazio
    const isEmpty = function (value) {
        return typeof value == 'string' && !value.trim() || typeof value == 'undefined' || value === null;
    }

    const init = () => {
        initTab()
        initForm()

        // Mete o atual csrf sempre que é efetuada uma mensagem ajax
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                const csrf = $('#csrf_token').val();
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf);
                }
            }
        });
    }

    //#region formulário
    //Inicializa o formulário, botões e ações
    const initForm = () => {
        $('#btn-login').on('click', login);
        $('#btn-registo').on('click', registo);
    }

    const login = function () {
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
                data: JSON.stringify({user: user, pass: pass}),
                success: (data, status, xhttp) => {
                    if (!data.success)
                        alert(data.msg)
                    console.log(data, status, xhttp)
                },
                error: (data, status, xhttp) => {
                    let response = data.responseJSON
                    if (response.CsrfError)
                        alert(response.msg)
                },
                contentType: "application/json",
                dataType: 'json'

            }
        )
    }

    const registo = function () {
        const user = $('#input-registo-username').val();
        const pass = $('#input-registo-password').val();

        //Verifica se os campos estao a vazio
        if (isEmpty(user) || isEmpty(pass)) {
            return alert('Por favor preencha todos os campos');
        }

        //manda o request para o registo
        $.ajax({
                type: "POST",
                url: 'registo',
                data: JSON.stringify({user: user, pass: pass}),
                success: (data, status, xhttp) => {
                    if (!data.success)
                        alert(data.msg)
                    console.log(data, status, xhttp)
                },
                error: (data, status, xhttp) => {
                    let response = data.responseJSON
                    if (response.CsrfError)
                        alert(response.msg)
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