angular.module('AnimeTracker').controller('indexCtrl', [
  '$scope', '$q', 'getAnimeList', 'getAnimeListSize', 'getAnimeSlice','searchAnime',
  function ($scope, $q, getAnimeList, getAnimeListSize, getAnimeSlice,searchAnime) {

    // Carousel
    $scope.myInterval = 5000;
    $scope.noWrapSlides = false;
    $scope.active = false;
    var slides = $scope.slides = [];
    var currIndex = 0;

    $scope.addSlide = function(url, text) {
      slides.push({
        image: url,
        text: text,
        id: currIndex++
      });
    };

    $scope.addSlide('/images/index_cover1.jpg','');
    $scope.addSlide('/images/index_cover2.jpg','');
    $scope.addSlide('/images/index_cover3.jpg','');


    // Anime List
    function datesort(a,b) {
      var t1 = a['timestamp'];
      var t2 = b['timestamp'];
      return t1 > t2 ? -1 : (t1 < t2 ? 1 : 0);
    }

    $scope.currentPage = 1;
    $scope.maxSize = 5;
    $scope.itemsPerPage = 60;
    $scope.currentAnimes = [];
    $scope.queryAnimes = [];
    $scope.cancelobj = undefined;

    getAnimeListSize(function(data){
      $scope.animes = [];
      $scope.totalItems = data.size;

      $scope.queryChanged = function(){
        if($scope.query && $scope.query.length > 1)
        {
          if($scope.cancelobj){
            $scope.cancelobj.resolve("search cancelled");
          }
          $scope.cancelobj = $q.defer();
          var request = searchAnime($scope.query, $scope.cancelobj, function(data){
            $scope.queryAnimes = data;
            $scope.cancelobj = undefined;
          });
        } else {
          $scope.queryAnimes = [];
        }
      };

      $scope.clearQuery = function(){
        $scope.query = '';
      };

      $scope.pageChanged = function(page){
        $scope.loadpage(page);
        $scope.currentPage = page;
      };

      $scope.loadpage = function(page){
        var index = (page - 1) * $scope.itemsPerPage;
        var ending = index + $scope.itemsPerPage;
        if(index < $scope.totalItems) {
          if(!$scope.animes[index]) {
            getAnimeSlice(index, ending, function(slice){
              for(var sv in slice){
                var iv = parseInt(sv);
                $scope.animes[index+iv] = slice[iv];
              }
              $scope.currentAnimes = $scope.animes.slice(index, ending);
            });
          } else {
            $scope.currentAnimes = $scope.animes.slice(index, ending);
          }
        }
      };

      $scope.loadpage($scope.currentPage);
    });

}]);
