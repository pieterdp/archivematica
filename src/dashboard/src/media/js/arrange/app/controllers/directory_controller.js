App.DirectoryController = Ember.Controller.extend({
    selected: false,
    open: false,

    actions: {
        toggleProperty: function(property) {
            this.toggleProperty(property);
        },
    },

});