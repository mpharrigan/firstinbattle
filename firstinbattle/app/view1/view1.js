'use strict';

angular.module('fibApp.view1', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/view1', {
            templateUrl: 'view1/view1.html',
            controller: 'View1Ctrl'
        });
    }])

    .controller('View1Ctrl', ['$scope', '$http', function ($scope, $http) {
        // TODO: Request this from server
        $scope.game_info = {
            card_info: {
                suits: ['heart', 'spade', 'club', 'diamond'],
                numbers: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            }
        };
        $scope.user = {name: 'player name', cards: [], pairs: []};
        $scope.req_card = {
            number: 11,
            suit: "heart"
        };
        $scope.req_from = {name: "", uuid: "0"};
        $scope.players = [];
        $scope.status = "Nothing happened yet";
        $scope.is_turn = false;
        $scope.is_registered = false;

        var protocolPrefix = (window.location.protocol === 'https:') ? 'wss:' : 'ws:';
        var ws = new WebSocket(protocolPrefix + '//' + location.host + '/gofish-ws');

        ws.onmessage = function (evt) {
            var data = JSON.parse(evt.data);
            switch (data.message) {
                case "player_registered":
                    $scope.$apply(function () {
                        $scope.user.name = data.user.name;
                        $scope.user.cards = data.cards;
                        $scope.status = "Player registered";
                        $scope.is_registered = true;
                    });
                    ws.send(JSON.stringify({
                        message: 'is_turn'
                    }));
                    ws.send(JSON.stringify({
                        message: 'get_players'
                    }));
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
                    ws.send(JSON.stringify({
                        message: 'consolidate_pairs'
                    }));
                    break;
                case "card_lost":
                    $scope.$apply(function () {
                        $scope.status = "You lost a card!";
                        $scope.user.cards = data.cards;
                    });
                    break;
                case "not_your_turn":
                    $scope.$apply(function () {
                        $scope.status = "It's not your turn!!";
                    });
                    break;
                case "is_turn":
                    $scope.$apply(function () {
                        $scope.is_turn = data.is_turn;
                    });
                    break;
                case "pairs_consolidated":
                    $scope.$apply(function () {
                        $scope.user.cards = data.cards;
                        $scope.user.pairs = data.all_pairs;
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
        };

        ws.onclose = function (evt) {
            $scope.$apply(function () {
                $scope.status = "Closed!";
                $scope.user = {name: 'closed', cards: []};
                $scope.is_registered = true;
                $scope.req_card = {
                    number: 11,
                    suit: "heart"
                };
                $scope.req_from = {name: "", uuid: "0"};
                $scope.players = [];
                $scope.is_turn = false;
            })
        };
    }]);