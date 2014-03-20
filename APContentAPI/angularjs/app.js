var searchText = "";
        var myapp = angular.module("myapp", ['ngSanitize'])
            .controller("Search", function ($scope, $http, $location) {
                //defaults
                $scope.searchText = "Tesla";
                $scope.mediaType = "photo";
                $scope.myData = {};
                doSearch();
                $scope.myData.doClick = function (item, event) {
                    doSearch();
                }
                //Search
                function doSearch() {
                    searchText = $scope.searchText;
                    var url = "http://api.ap.org/v2/search/" + $scope.mediaType + "?apikey=your_api_key&q=" + $scope.searchText + "&callback=JSON_CALLBACK";
                    var responsePromise = $http({ method: 'jsonp', url: url });

                    responsePromise.success(function (data, headers) {
                        $scope.myData.fromServer = data;
                        //console.log($location);
                    });
                    responsePromise.error(function (data, status, headers, config) {
                        console.log(status);
                        alert("AJAX failed!");
                    });
                }
            });
        //Custom Filters
        myapp.filter('highlighter', function () {
            return function (t) {
                if (t != null) {
		            var highlightedText = "<b class='highlighted'>" + searchText + "</b>";
					var searchExpr = "/" + searchText + "/g";
					retval = t.replace(eval(searchExpr),highlightedText);
                    console.log(searchExpr);
                    return retval;
                }
            }
        });

        function ContentApiCtrl($scope) {
            $scope.hellomessage = "AP Content Search Example";
        }