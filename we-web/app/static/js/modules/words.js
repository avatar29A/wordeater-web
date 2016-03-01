/**
 * Created by Warlock on 21.02.2016.
 */

var Words = (function() {
    var self = {};
    self.vm = undefined;

    self.init = function () {
        self.loadViewModel();
    };

    self.loadViewModel = function () {
        $LAB.script("/static/js/viewmodels/words_vm.js").wait(self.initViewModel);
    };

    self.initViewModel = function () {
        self.vm = WordsViweModel();
        ko.applyBindings(self.vm);
        self.loadGroups();
    };

    self.loadGroups = function(){
      Get('/api/learn/groups/', function(response){
          self.vm.setGroups(response.data);
      })
    };

    return self;
}());

$(function(){
   Words.init();
});