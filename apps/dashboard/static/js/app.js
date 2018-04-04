// Grafico de barra
// Grafico de linha
function get_diary() {
    $.ajax({
        method: "GET",
        url: "http://autopolar.canionlabs.io/api/production/?format=json",
        dataType: "json"
    })
        .done(function(json) {
            console.log(json)
        })
        .fail(function(msg) {
          console.log(msg);
        });
};

get_diary()
