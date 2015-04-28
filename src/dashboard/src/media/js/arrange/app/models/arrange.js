
App.Directory = DS.Model.extend({
   name: DS.attr('string'),
   open: DS.attr('boolean'),
   type: DS.attr('string'),
});

App.Directory.FIXTURES = [
    {
        id: 1,
        name: 'sip-uuid',
        type: 'directory',
    },
    {
        id: 2,
        name: 'open-sip-uuid',
        type: 'directory',
    },
    {
        id: 3,
        name: 'another sip',
        type: 'directory',
    },
    {
        id: 4,
        name: 'look a file',
        type: 'file',
    }
]