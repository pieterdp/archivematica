Arrange.DirectoryController = Ember.ObjectController.extend({
    selected: false,
    open: false,

    actions: {
        toggleProperty: function(property) {
            this.toggleProperty(property);
        },
    },

});