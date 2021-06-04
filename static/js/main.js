$(document).ready(function () {
    $('.image-section').hide();
    $('.loader').hide();

    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e)
            {
            var x = document.createElement("IMG");
            x.setAttribute("src", e.target.result);
            x.setAttribute("align","right");
            x.setAttribute("width", "304");
            x.setAttribute("height", "228");
            x.setAttribute("alt", "The Pulpit Rock");

            $("#dcm").html(x);
                console.log("LOADER EXECUATED");

                $('.loader').hide();
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();

        readURL(this);
    });


function removeElement(ele) {
    ele.parentNode.removeChild(ele);
                        }

    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        $(this).show();
        $('.loader').show();

        $.ajax({
				type: 'POST',
				url: '/predict',
				data: form_data,
				contentType: false,
				cache: false,
				processData: false,
				async: true,
				success: function (data) {
				var x = document.createElement("IMG");
				x.setAttribute("src", '/static/image.png');
                x.setAttribute("align","right");
				x.setAttribute("width", "304");
				x.setAttribute("height", "228");
				x.setAttribute("alt", "The Pulpit Rock");

        $("#divResult").html(x);
                console.log("LOADER EXECUATED");

                $('.loader').hide();

                console.log('Success!');
            },
        });
    });


});



