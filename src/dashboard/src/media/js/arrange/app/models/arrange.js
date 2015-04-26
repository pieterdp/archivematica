
Arrange.Directory = DS.Model.extend({
   name: DS.attr('string'),
   open: DS.attr('boolean'),
   type: DS.attr('string'),
});

Arrange.Directory.FIXTURES = [
    {
        id: 1,
        name: 'sip-uuid',
        open: false,
        type: 'directory',
    },
    {
        id: 2,
        name: 'open-sip-uuid',
        open: true,
        type: 'directory',
    },
    {
        id: 3,
        name: 'another sip',
        open: true,
        type: 'directory',
    },
    {
        id: 4,
        name: 'look a file',
        open: null,
        type: 'file',
    }
]