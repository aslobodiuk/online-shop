function disable_form($form) {
    $form.find('input').prop('disabled', true);
}

$(document).ready(function(){
    $form = $('#filter_form')
    $('.inp').change(function(){
        $('#submit').click();
        disable_form($form);
    });
});