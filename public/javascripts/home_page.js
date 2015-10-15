var animelistdata = [];
var colorCollection = ["bc-glass","bc-tree","bc-green","bc-blue","bc-silly","bc-sand","bc-mustard","bc-powder","bc-blush","bc-cranesbill","bc-blue"];

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

        animelistdata = data;

        anime_container.empty();
        $.each(data, function() {
            if(index % 6 == 0) {
                current_row = $('<div class="row anime-row"></div>')
                anime_container.append(current_row);
            }
            current_row.append(new AnimeItem(this.name, this._id).htmlElem);
            index++;
        });

        $('div#anime_container div.anime-item a.btn-detail').click(onClickAnime);
        $('div#anime_container div.anime-item a.btn-download').click(onClickDownloadAll);
    });
}

function AnimeItem(name, id) {
    var col = $('<div class="col-sm-2"></div>');
    var content = $('<div class="anime-item center-block"></div>');
    var detail = $('<div class="anime-item-title center-block"><h4 class="text-center">' + name + '</h4></div><p class="text-center"><a rel="' + id + '" class="btn btn-default btn-download" href="#" role="button">Download All</a></p><p class="text-center"><a rel="' + id + '" class="btn btn-default btn-detail" href="#" role="button" data-loading-text="Loading...">Details</a></p>');
    var color_index = Math.round(Math.random()*10);
    content.addClass(colorCollection[color_index]);
    col.append(content.append(detail));
    this.htmlElem = col;
}

function onClickAnime(event) {
    var btn = $(this);
    btn.button('loading');
    // Prevent Link from Firing
    event.preventDefault();

    // Retrieve username from link rel attribute
    var id = $(this).attr('rel');

    $.getJSON( '/animes/videos/'+id, function( data ) {
        var modal_content =  $('#modal_content');
        
        modal_content.empty();

        $.each(data, function(){
            var dl_links = "";
            $.each(this.dl_url,function(index, elem){
                dl_links += '<a href="'+elem+'"> Download' + (index + 1).toString() +' </a>';
            });
            modal_content.append($('<div class="row"></div>').append($('<div class="col-sm-8"></div>').append($('<h4>' + this.name + '</h5>'))).append($('<div class="col-sm-4"></div>').append($(dl_links))));
            modal_content.append($('<hr class="anime-hr">'));
        });

        $('hr.anime-hr:last').remove();

        $('#animeDetailModal').modal('toggle');

        btn.button('reset');

    });
}

function onClickDownloadAll(event) {
    // Prevent Link from Firing
    event.preventDefault();

    // Retrieve username from link rel attribute
    var id = $(this).attr('rel');

    $.getJSON( '/animes/videos/'+id, function( data ) {
        var thunder_str = "";
        var pid = Math.floor(Math.random()*10000);

        BatchTasker.BeginBatch(4,pid);    //开始批量添加

        $.each(data, function(){
            thunder_str += this.dl_url[0] + '\n';
            BatchTasker.AddTask(this.dl_url[0], this.name, "", this.name, "", 1, 1, 10);   //添加下载任务2
        });
        console.log(thunder_str);

        BatchTasker.EndBatch(pid);
    });
}
