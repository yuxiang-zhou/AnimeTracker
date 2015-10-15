var animelistdata = [];

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

        $('div#anime_container div.anime-item a.btn').click(onClickAnime);
    });
}

function AnimeItem(name, id) {
    var col = $('<div class="col-sm-2"></div>');
    var content = $('<div class="anime-item center-block"><div class="anime-item-title center-block"><h4 class="text-center">' + name + '</h4></div><p class="text-center"><a rel="' + id + '" class="btn btn-default" href="#" role="button">Details</a></p></div>');
    col.append(content);
    this.htmlElem = col;
}

function onClickAnime(event) {
    // Prevent Link from Firing
    event.preventDefault();

    // Retrieve username from link rel attribute
    var id = $(this).attr('rel');

    $.getJSON( '/animes/videos/'+id, function( data ) {
        console.log(data);
    });
}
