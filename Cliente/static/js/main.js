var IndexHelper = function () {

    const initTab = () => {
        let tabs = $('.tab-item')
        $.each(tabs,(i,v) => {
            $(v).on('click',function(){
                const tabName = $($(this).find('a')[0]).data('tab')
                changeTab(this,tabName)
                $(this).addClass('active')
            })
        })
    }

    const changeTab = (v,tabName) => {
        $('.tab-content').hide()
        $('.tab-item').removeClass('active')
        $('#' + tabName).show()
        $(this).addClass('active')
    }

    return {
        initTab: initTab
    }
}()

$(function () {
    IndexHelper.initTab()
})