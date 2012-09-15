"use strict"

# Declare app level module which depends on filters, and services
angular.module("myApp", ["myApp.filters", "myApp.services", "myApp.directives"]).config ["$routeProvider", ($routeProvider) ->
  $routeProvider.when "/",
    templateUrl: "partials/main.html"
    controller: MainCtrl

  $routeProvider.when "/start",
    templateUrl: "partials/start.html"
    controller: StartCtrl

  $routeProvider.when '/document',
    templateUrl: 'partials/document.html'
    controller: DocCtrl

  $routeProvider.otherwise redirectTo: "/"
]