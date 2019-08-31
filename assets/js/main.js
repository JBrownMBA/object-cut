// Dropdown
$('.form .dropdown').dropdown();

// Checkbox
$('#input-file').hide();
$('.form .checkbox').checkbox();
$('.form .checkbox').checkbox({
    onChecked: function () {
        if ($('#from-url').is(':checked')) {
            $('#input-file').hide();
            $('#input-url').show();
        } else {
            $('#input-url').hide();
            $('#input-file').show();
        }
    }
});