// Generated by CoffeeScript 1.3.3
"use strict";

angular.module("myApp.directives", []).directive("appVersion", [
  "version", function(version) {
    return function(scope, elm, attrs) {
      return elm.text(version);
    };
  }
]);