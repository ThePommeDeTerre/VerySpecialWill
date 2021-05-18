// Controlador do index
const IndexHelper = function () {
    const init = () => {
        initForm()
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

    //Funcao para ajudar a ver se está vazio (because javascript)
    const isEmpty = function (value) {
        return typeof value == 'string' && !value.trim() || typeof value == 'undefined' || value === null;
    }

    Date.prototype.toDateInputValue = (function () {
        var local = new Date(this);
        local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
        return local.toJSON().slice(0, 10);
    });

    //#region formulário
    //Inicializa o formulário, botões e ações
    const initForm = () => {
        setupAjax()
        $('#input-allowed_date').val(new Date().toDateInputValue());
        $('#btn-add-user').on('click', add_user)
        $("#users-table").on('click', 'button', delete_user)
        $('#btn-submit').on('click', test_form);
    }

    const handleAjaxError = (data) => {
        const divMessages = $('#alert-messages');
        divMessages.html('')

        let message = data.msg ? data.msg : ''

        let errorDiv = $('<div>')
        errorDiv.addClass('toast toast-error').text(message)
        divMessages.append(errorDiv)

    }

    const test_form = function (event) {
        let element = $(event.currentTarget)
        element.attr('disabled', true)

        let date = $('#input-allowed_date').val(),
            n_shares = $('#input-number_of_shares').val(),
            min_shares = $('#input-minimum_shares').val(),
            special_will = $('#input-special_will').val(),
            emailList = $('#input-user_multiple').val()

        if (isEmpty(n_shares) || isEmpty(min_shares) || isEmpty(special_will) || isEmpty(date) || isEmpty(emailList)) {
            alert('Please fill all fields')
            return false;
        }
        if (n_shares == 0 || min_shares == 0) {
            alert('Shares values can\'t be 0')
            return false;
        }

        let date_input = new Date(date)
        let date_today = new Date()
        date_today.setDate(date_today.getDate() - 1)

        if (date_today > date_input) {
            alert('Chosen date can\'t be before today')
            return false;
        }

        if (n_shares < min_shares) {
            alert('Number of shares must be superior or equal to number of minimum shares')
            return false;
        }

        if (emailList.length < n_shares) {
            alert('Number of emails must be the same as number of shares')
            return false;
        }

        let params = {
            cypher: $('#input-cypher_type').val(),
            hash: $('#input-hash_function').val(),
            date: date,
            n_shares: n_shares,
            min_shares: min_shares,
            special_will: special_will,
            emailList: emailList
        }

        //manda o request para o login
        $.ajax({
                type: "POST",
                url: '/createwill',
                data: JSON.stringify(params),
                success: (data, status) => {
                    // Retira o disabled
                    element.attr('disabled', false)
                    if (!data.success)
                        handleAjaxError(data)
                    else
                        window.location.replace("/inheritedwills");
                },
                error: (data) => {
                    // Retira o disabled
                    element.attr('disabled', false)
                    handleAjaxError(data.responseJSON)
                },
                contentType: "application/json",
                dataType: 'json'
            }
        )


        alert('success')
    }

    /*adiciona à tabela*/
    const add_user = function () {
        /*Verifica se o email é valido*/
        if (!$('#input-user_to_add').is(':valid')) {
            alert('Invalid Email to Add')
            return
        }

        let email = $('#input-user_to_add').val()
        let emailList = $('#input-user_multiple').val()

        emailList.push(email)

        $('#input-user_multiple').append(new Option(email, email));
        $('#input-user_multiple').val(emailList)
        update_table(emailList)

    }

    const update_table = function (emailList) {
        /*limpa a tabela*/
        $("#users-table").find('tbody').html('')

        /*faz append a tabela, adicionando o email e um botão para o remover*/
        $.each(emailList, (i, val) => {
            $("#users-table").find('tbody')
                .append($('<tr>')
                    .append($('<td>')
                        .append($('<span>')
                            .text(val)
                        )
                    ).append($('<td>')
                        .append($('<button>')
                            .addClass('btn btn-error')
                            .data('email', val)
                            .attr('type', 'button')
                            .text('remove')
                        )
                    )
                );
        })

    }

    /*apaga um utilizador da tabela e atualiza a lista*/
    const delete_user = function (event) {
        let element = $(event.currentTarget),
            select_element = $('#input-user_multiple'),
            email = element.data('email'),
            emailList = select_element.val(),
            index = emailList.indexOf(email)
        $("#input-user_multiple option[value='" + email + "']").remove();
        if (index !== -1) {
            emailList.splice(index, 1);
        }
        update_table(emailList)
    }

//#endregion

    return {
        init: init,
        delete_user: delete_user
    }
}
();

$(function () {
    IndexHelper.init()
})