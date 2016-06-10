'use strict';
/**
 * @ngdoc overview
 * @name marketApp
 * @description
 * # marketApp
 *
 * Main module of the application.
 */
var app = angular
  .module('AnimeTracker', [
    'ngAnimate',
    'ui.router',
    'ui.bootstrap',
    'servData'
  ])
  .config(['$stateProvider','$urlRouterProvider','$compileProvider',
  function ($stateProvider,$urlRouterProvider,$compileProvider) {

    $compileProvider.debugInfoEnabled(false);

    $urlRouterProvider.when('', '/anime/index');
    $urlRouterProvider.when('/', '/anime/index');
    $urlRouterProvider.otherwise('/notfound');

    $stateProvider
      .state('home', {
        url:'/anime',
        templateUrl: 'views/template.html',
      }).state('home.index',{
        url:'/index',
        // controller: 'indexCtrl',
        templateUrl:'views/index.html',
      })
  }])

.run(['$rootScope', '$location','$http', '$state', '$stateParams',
  function ($rootScope, $location, $http, $state, $stateParams) {

  }]);
