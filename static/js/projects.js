
var app = angular.module('myApp', []);
app.config(['$interpolateProvider', function($interpolateProvider) {
$interpolateProvider.startSymbol('{[');
$interpolateProvider.endSymbol(']}');
}]);

app.controller('ProjectListCtrl', function ($scope, $http){
    $http.get('/ang_form').success(function(data){
        $scope.projects = data;
    })
});