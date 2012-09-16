'use strict'

# Controllers 
MainCtrl = ($scope, $window) ->

StartCtrl = ($scope) ->

DocCtrl = ($scope, $location, $window) ->
  $scope.documentUploaded = false
  $scope.upload = () ->
    $scope.$apply ->
      $scope.documentUploaded = true
  $scope.submit = ->
    getGoals = ->
      $.post 'api/getGoals',
        'sessionID': $window.sessionID,
        (data) ->
          $window.documentGame = {} 
          $window.documentGame.start = data.start 
          $window.documentGame.end = data.end
          $location.path('/documents/' + data.nextDocument)
        'json'

    poll = ->
      $.post 'api/getStatus',
        'sessionID': $window.sessionID,
        (data) ->
          if data != 'ready'
            #setTimeout(poll(), 2000)
          else
            getGoals()

    createSession = (data) ->
      $window.sessionID = data
      poll()


    $.post "api/createSession", 
      'gameType': 'document'
      'userID': String(FB.getUserID()),
      createSession(data)

DocsCtrl = ($scope, $routeParams) ->
  processDocument = (data) ->
    

  $scope.documentID = $routeParams.documentID
  $scope.start = $window.documentGame.start
  $scope.end = $window.documentGame.end
  $.get 'api/getDocument',
    'documentID': $scope.documentID
    processDocument(data)


MyCtrl2 = ->


# MainCtrl.$inject = []
# MyCtrl2.$inject = []