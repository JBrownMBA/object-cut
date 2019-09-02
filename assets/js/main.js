// Init
$('#error-message').hide();
$('#success-message').hide();
$('#card-result').hide();
$('.form #input-file').hide();

// Animations
$('#form-card').hide();
setTimeout(function() {$('#form-card').transition('scale');}, 250);

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

// Message
$('#error-message .close').on('click', function() {$('#error-message').transition('horizontal flip');})
$('#success-message .close').on('click', function() {$('#success-message').transition('horizontal flip');})

function showErrorMessage(message) {
    if ($('#success-message').is(":visible")) {
        $('#success-message').transition('horizontal flip');
    }
    $('.error-messsage-text').html(message);
    if ($('#error-message').is(":hidden")) {
        $('#error-message').transition('horizontal flip');
    }
}

function showSuccessMessage(message) {
    if ($('#error-message').is(":visible")) {
        $('#error-message').transition('horizontal flip');
    }
    $('.success-messsage-text').html(message);
    if ($('#success-message').is(":hidden")) {
        $('#success-message').transition('horizontal flip');
    }
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
            showSuccessMessage('Your image was successfully loaded.')
        };
        reader.onerror = function (e) {
            showErrorMessage('Wrong uploaded image.');
            $('.form').removeClass('loading');
        }
        reader.readAsDataURL(input.target.files[0]);
    } else {
        showErrorMessage('Wrong uploaded image.');
        $('.form').removeClass('loading');
    }
});

// Ajax
function callApi(formData) {
    $('.form').addClass('loading');
    $.ajax({
        type: 'POST',
        url: 'https://objectapi.ga/cut',
        data: JSON.stringify(formData),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data) {
            $('#form-card').transition('scale');
            $('#card-result img').attr('src', 'data:image/png;base64,' + data.response.image_base64);
            setTimeout(function() {$('#card-result').transition('slide down');}, 500);
        },
        error: function() {
            showErrorMessage('Try again, please.');
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
            showErrorMessage('No image URL specified.');
        } else {
            formData['image_url'] = imageUrl;
            callApi(formData);
        }
    } else {
        imageBase64 = getFieldValueInput('imageBase64');
        if (!imageBase64) {
            showErrorMessage('No file uploaded.');
        } else {
            formData['image_base64'] = imageBase64;
            callApi(formData);
        }
    }
});