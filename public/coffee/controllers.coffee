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
          if data.status != 'Ready'
            setTimeout( ->
                poll()
              2000)
          else
            getGoals()
    poll()

DocsCtrl = ($scope, $routeParams, $window) ->
  processDocument = (data) ->
    # doc = data.text.linkForPositions(data.keywords)
    doc = data.text.linkForPositions ['location': 5, 'length': 10]
    converter = new Markdown.Converter()
    $($('.document-view')[0]).html(converter.makeHtml(doc))

  $scope.documentID = $routeParams.documentID
  $window.documentGame = {}
  # $scope.start = $window.documentGame.start
  # $scope.end = $window.documentGame.end
  # $.get 'api/getDocument',
  #   'documentID': $scope.documentID
  #   processDocument(data)
  $.post 'api/getDocument',
    'keyword': 'questions',
    (data)->
      processDocument(data)
    
  $('div.document-view > a').on 'click', (event)->
    console.log event


# MainCtrl.$inject = []
# MyCtrl2.$inject = []