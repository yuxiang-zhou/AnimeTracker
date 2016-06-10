angular.module('servData', []).factory(
  'getAnimeList', ['$http',
  function($http) {
    return function(onSuccess){
      var query = '/api/animelist/';
      $http.get(query, { cache: true }).success(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'getAnime', ['$http',
  function($http) {
    return function(id, onSuccess){
      var query = '/api/anime/' + id;
      $http.get(query, { cache: true }).success(function(data){
        onSuccess(data);
      });
    }
  }]
);
