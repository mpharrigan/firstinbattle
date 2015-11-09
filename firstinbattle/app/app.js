'use strict';

// Declare app level module which depends on views, and components
angular.module('fibApp', [
    'ngRoute',
    'fibApp.view1',
    'fibApp.view2'
]).
config(['$routeProvider', function ($routeProvider) {
    $routeProvider.otherwise({redirectTo: '/view1'});
}]);
