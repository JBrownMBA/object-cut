// Init
$('#error-message').hide();
$('#card-result').hide();
$('.form #input-file').hide();

// Form retrieving
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

// Base64
$('#file').on('change', function(input) {
    $('.form').addClass('loading');
    if (input.target.files && input.target.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            resultSplit = e.target.result.split(',');
            resultSplit.shift();
            $(".form input[name=imageBase64]").val(resultSplit.join());
            $('.form').removeClass('loading');
        };
        reader.onerror = function (e) {
            $('.error-messsage-text').html('Wrong uploaded image.')
            $('#error-message').show();
            $('.form').removeClass('loading');
        }
        reader.readAsDataURL(input.target.files[0]);
    } else {
        $('.error-messsage-text').html('Wrong uploaded image.')
        $('#error-message').show();
        $('.form').removeClass('loading');
    }
});

// Ajax
function callApi(formData) {
    $('.form').addClass('loading');
    $.ajax({
        type: 'POST',
        url: 'http://134.209.244.212:8083/cut',
        data: JSON.stringify(formData),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data) {
            $('#form-card').hide();
            $('#card-result img').attr('src', 'data:image/png;base64,' + data.response.image_base64);
            $('#card-result').show();
        },
        failure: function(errMsg) {
            $('.error-messsage-text').html('Try again, please.')
            $('#error-message').show();
        },
        complete: function() {
            $('.form').removeClass('loading');
        }
    });
}

// Form
$('.form button').on('click', function() {
    $('#error-message').hide();
    var formData = {
        objects: getFieldValueSelect('objects'),
        return_bounding_box: getFieldValueCheckbox('boundingBox'),
        return_text: getFieldValueCheckbox('text'),
        return_white_bg: getFieldValueCheckbox('whiteBg')
    };
    if ($('#from-url').is(':checked')) {
        imageUrl = getFieldValueInput('imageUrl')
        if (!imageUrl) {
            $('.error-messsage-text').html('No image URL specified.')
            $('#error-message').show();
        } else {
            formData['image_url'] = imageUrl;
            callApi(formData);
        }
    } else {
        imageBase64 = getFieldValueInput('imageBase64');
        if (!imageBase64) {
            $('.error-messsage-text').html('No file uploaded.')
            $('#error-message').show();
        } else {
            formData['image_base64'] = imageBase64;
            callApi(formData);
        }
    }
});

// Message
$('#error-message .close').on('click', function() {$('#error-message').hide();})