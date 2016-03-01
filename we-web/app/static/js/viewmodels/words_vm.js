/**
 * Created by Warlock on 21.02.2016.
 */

function WordsViweModel() {
    var self = {};

    self.groups = ko.observableArray([]);

    self.setGroups = function(groups) {
        self.groups(groups);
        console.log(groups);
    };
    return self;
}