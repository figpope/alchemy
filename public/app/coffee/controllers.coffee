'use strict'

# Controllers 
MainCtrl = ($scope, $window) ->
  $scope.loginStatus = 'loading..'
  $window.fbUpdate = ->
    FB.getLoginStatus (response) ->
      console.log 'ran'
      $scope.loginStatus = response.status
      if response.status is "connected"
        # the user is logged in and has authenticated your
        # app, and response.authResponse supplies
        # the user's ID, a valid access token, a signed
        # request, and the time the access token 
        # and signed request each expire
        uid = response.authResponse.userID
        accessToken = response.authResponse.accessToken
      else if response.status is "not_authorized"
        # the user is logged in to Facebook, 
        # but has not authenticated your app
      else
        # the user isn't logged in to Facebook.

MyCtrl2 = ->


# MainCtrl.$inject = []
# MyCtrl2.$inject = []