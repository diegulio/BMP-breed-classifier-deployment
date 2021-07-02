function BreedPredict(){
    console.log("Breed prediction clicked");

    var image = document.getElementById('ImageInput')
    console.log(image);

    var result = document.getElementById('predict')

    var url = "/predict"


    $.post(
        url,
        {
            image: image
        },
        function (data, status){
            result.innerHTML = '<div class="alert alert-success" id = "respuesta_text">' + data.result + '</div>';

        }
    );



}
