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
          getAnime($scope.anime._id, function(response){
            $scope.anime = response;
          });
        };

        $scope.hasVideo = function(videos){
          return videos && Object.keys(videos).length > 0;
        };
      },
      link: function($scope, elem, attrs){

      }
    }
  }
]);
