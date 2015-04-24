
Arrange.Directory = DS.Model.extend({
   name: DS.attr('string'),
   open: DS.attr('boolean')
});

Arrange.Directory.FIXTURES = [
    {
        id: 1,
        name: 'sip-uuid',
        open: false
    },
    {
        id: 2,
        name: 'open-sip-uuid',
        open: true
    },
    {
        id: 3,
        name: 'another sip',
        open: true
    }
]