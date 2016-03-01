/**
 * Created by Warlock on 21.02.2016.
 */

var RestAPI = (function() {
    var self = {};
    self.resource_url = "";

    self.list = function (success, error, cbFinally) {
        Get(self.resource_url, success, error, {
            cbFinally: cbFinally
        });
    };

    self.get = function (id, success, error, cbFinally) {
        Get(self.resource_url + '/' + id, success, error, {
            cbFinally: cbFinally
        });
    };

    self.create = function (data, success, error, cbFinally) {
        Post(self.resource_url, data, success, error, {
            cbFinally: cbFinally
        })
    };

    self.save = function (id, data, success, error, cbFinally) {
        Patch(self.resource_url + '/' + id, data, success, error, {
            cbFinally: cbFinally
        });
    };

    self.delete = function (success, error, cbFinally) {
        Delete(self.resource_url, success, error, {
            cbFinally: cbFinally
        })
    };

    return self;
});