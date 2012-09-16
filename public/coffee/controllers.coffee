'use strict'

# Controllers 
GameCtrl = ($scope) ->
  $scope.userPoints = 0

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
            setTimeout( ->
                poll()
              2000)
          else
            getGoals()
    poll()

DocsCtrl = ($scope, $routeParams) ->
  processDocument = (data) ->
    doc = data.doc.linkForPositions(data.positions)
    converter = new Markdown.Converter()
    $($('.document-view')[0]).html(converter.makeHtml(doc))

  $scope.documentID = $routeParams.documentID
  $scope.start = $window.documentGame.start
  $scope.end = $window.documentGame.end
  $.get 'api/getDocument',
    'documentID': $scope.documentID
    processDocument(data)
  $.on 'click', 'div.document-view > a', (event)->
    console.log event


# MainCtrl.$inject = []
# MyCtrl2.$inject = []