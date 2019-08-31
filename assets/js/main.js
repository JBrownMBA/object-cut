// Semantic
function getFieldValueInput(fieldId) { 
    return $(".form input[name=" + fieldId + "]").val();
}

function getFieldValueCheckbox(fieldId) { 
    return $(".form input[name=" + fieldId + "]").is(':checked');
}

function getFieldValueSelect(fieldId) { 
    return $(".form select[name=" + fieldId + "]").val();
}

// Dropdown
$('.form .dropdown').dropdown();

// Checkbox
$('.form #input-file').hide();
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

// Form
$('.form button').on('click', function() {
    var formData = {
        objects: getFieldValueSelect('objects'),
        return_bounding_box: getFieldValueCheckbox('boundingBox'),
        return_text: getFieldValueCheckbox('text'),
        return_white_bg: getFieldValueCheckbox('whiteBg')
    };
    if ($('#from-url').is(':checked')) {
        imageUrl = getFieldValueInput('imageUrl')
        if (!imageUrl) {
            console.log('[ERROR] No image URL');
            return;
        } else {
            formData['image_url'] = imageUrl;
        }
    } else {
        imageBase64 = getFieldValueInput('imageBase64');
        if (!imageBase64) {
            console.log('[ERROR] No imageBase64');
            return;
        } else {
            formData['image_base64'] = imageBase64;
        }
    }
    console.log(formData);
    $('.form').addClass('loading');
});
