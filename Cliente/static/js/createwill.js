// Controlador do index
const IndexHelper = function () {
    const init = () => {
        initForm()
    }

    //#region formulário
    //Inicializa o formulário, botões e ações
    const initForm = () => {
        $('#btn-add-user').on('click', add_user)
    }

    const add_user = function(){
        debugger
        let email = $('#input-user_to_add').val()
        let emailList = $('#input-user_multiple').val()

        emailList.push(email)

        $('#input-user_multiple').append(new Option(email, email));
        $('#input-user_multiple').val(emailList)

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