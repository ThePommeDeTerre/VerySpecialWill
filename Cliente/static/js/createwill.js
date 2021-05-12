// Controlador do index
const IndexHelper = function () {
    const init = () => {
        initForm()
    }

    //#region formulário
    //Inicializa o formulário, botões e ações
    const initForm = () => {
        $('#btn-add-user').on('click', add_user)

        $("#users-table").on('click', 'button', delete_user)
    }

    /*adiciona à tabela*/
    const add_user = function () {
        /*Verifica se o email é valido*/
        if (!$('#input-user_to_add').is(':valid') ){
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