App.ArrangeController = Ember.ArrayController.extend({
    actions: {
        deaccession: function () {
            // FIXME What do I delete here?
            // Can I get it to pass a param of the selected?
        }
    },

    // File and directory count display
    file_count: function() {
        return this.filterBy('type', 'file').get('length');
    }.property('@each.type'),
    file_inflection: function() {
        var file_count = this.get('file_count');
        return file_count === 1 ? 'file' : 'files';
    }.property('file_count'),
    directory_count: function() {
        return this.filterBy('type', 'directory').get('length');
    }.property('@each.type'),
    directory_inflection: function() {
        var directory_count = this.get('directory_count');
        return directory_count === 1 ? 'directory' : 'directories';
    }.property('directory_count'),
});