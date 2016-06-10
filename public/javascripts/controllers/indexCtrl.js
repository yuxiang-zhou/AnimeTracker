angular.module('AnimeTracker').controller('indexCtrl', [
  '$scope', 'getAnimeList',
  function ($scope, getAnimeList) {

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
    getAnimeList(function(data){
      $scope.animes = data;
    });

}]);
