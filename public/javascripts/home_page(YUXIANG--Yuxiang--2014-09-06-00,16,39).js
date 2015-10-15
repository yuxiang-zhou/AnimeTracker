$(function(){
    // Index Page Initialisation

    LoadAnimeList();
});

function LoadAnimeList() {
    // Empty content string
    // jQuery AJAX call for JSON
    $.getJSON( '/animes/animelist', function( data ) {

        // For each item in our JSON, add a table row and cells to the content string
        var index = 0;
        var anime_container = $("#anime_container");
        var current_row;

        anime_container.empty();
        $.each(data, function() {
            if(index % 6 == 0) {
                current_row = $('<div class="row anime-row"></div>')
                anime_container.append(current_row);
            }
            current_row.append(new AnimeItem(this.name, this._id).htmlElem);
            index++;
        });
    });

    $('#anime_container div.col-sm-2').on('click', 'a.btn', deleteUser);
}

function AnimeItem(name, id) {
    var col = $('<div class="col-sm-2"></div>');
    var content = $('<div class="anime-item center-block"><div class="anime-item-title center-block"><h4 class="text-center">' + name + '</h4></div><p class="text-center"><a rel="' + id + '" class="btn btn-default" href="#" role="button">Details</a></p></div>');
    col.append(content);
    this.htmlElem = col;
}