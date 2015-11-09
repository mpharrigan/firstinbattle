'use strict';

angular.module('fibApp.view1', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/view1', {
            templateUrl: 'view1/view1.html',
            controller: 'View1Ctrl'
        });
    }])

    .controller('View1Ctrl', ['$scope', '$http', function ($scope, $http) {
        $scope.user = {name: 'notset', cards: []};
        $scope.req_card = {
            number: 12,
            suit: "hearts"
        };
        $scope.req_from = {name: 'notset'};
        $scope.players = [];
        $scope.status = "Nothing happened yet";
        var ws = new WebSocket("ws://localhost:7777/gofish-ws");

        ws.onmessage = function (evt) {
            var data = JSON.parse(evt.data);
            switch (data.message) {
                case "player_registered":
                    $scope.$apply(function () {
                        $scope.user.cards = data.cards;
                    });
                    console.log("User was registered " + data.cards);
                    break;
                case "return_players":
                    $scope.$apply(function () {
                        $scope.players = data.players;
                    });
                    break;
                case "receive_card":
                    $scope.$apply(function () {
                        $scope.user.cards.push(data.card);
                        if (data.success) {
                            $scope.status = "You took one!";
                        } else {
                            $scope.status = "Go fish!";
                        }
                    });
                    break;
                default:
                    console.log("Unknown message " + data.message)
            }
        };

        $scope.new_game = function (user) {
            $scope.user = angular.copy(user);
            ws.send(JSON.stringify(
                {message: 'register_player', user: user}
            ));
        };

        $scope.request_card = function () {
            ws.send(JSON.stringify(
                {
                    message: 'request_card',
                    card: $scope.req_card,
                    from: $scope.req_from
                }
            ));
        }
    }]);