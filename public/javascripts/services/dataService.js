angular.module('servData', []).factory(
  'getAnimeList', ['$http',
  function($http) {
    return function(onSuccess){
      var query = '/api/animelist/';
      return $http.get(query).success(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'getAnimeListSize', ['$http',
  function($http) {
    return function(onSuccess){
      var query = '/api/animelistsize/';
      return $http.get(query).success(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'getAnimeSlice', ['$http',
  function($http) {
    return function(vfrom,vto,onSuccess){
      var query = '/api/animelist/' + vfrom + '/' + vto;
      return $http.get(query).success(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'getAnime', ['$http',
  function($http) {
    return function(id, onSuccess){
      var query = '/api/anime/' + id;
      return $http.get(query).success(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'searchAnime', ['$http',
  function($http) {
    return function(name, timeout, onSuccess){
      var query = '/api/anime/search/' + name;
      return $http.get(query, {timeout: timeout.promise}).success(function(data){
        onSuccess(data);
      });
    }
  }]
);
