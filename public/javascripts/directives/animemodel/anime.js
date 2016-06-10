angular.module('AnimeTracker').directive('anime',
  ['$rootScope', 'getAnime',
  function($rootScope, getAnime) {
    return {
      templateUrl: 'javascripts/directives/animemodel/anime.html',
      replace: true,
      restrict: 'E',
      scope: {
        anime: '='
      },
      controller: function($scope){
        $scope.loaddetails = function(){
          if(!$scope.anime.videos) {
            getAnime($scope.anime._id, function(response){
              $scope.anime = response;
            });
          }
        }
      },
      link: function($scope, elem, attrs){

      }
    }
  }
]);
