App.Directory = DS.Model.extend
    title: DS.attr('string')
    children: DS.hasMany('directory', {async: true})
    parent: DS.belongsTo('directory', {async: true})

App.Directory.FIXTURES = [
    {id: 1, title: 'Family', parent: 0, children: [10, 11]},
    {id: 10, title: 'Susan', parent: [1], children: [100, 101]},
    {id: 11, title: 'Luda', parent: [1], children: [102, 103]},
    {id: 100, title: 'Josh', parent: [10], children: []},
    {id: 101, title: 'Moses', parent: [10], children: []},
    {id: 102, title: 'Verdi', parent: [11], children: []},
    {id: 103, title: 'Gaya', parent: [11], children: []},
]

// App.Directory = DS.Model.extend({
//    title: DS.attr('string'),
//    type: DS.attr('string'),
//    children: DS.hasMany('tag', {async: true}),
//    parent: DS.belongsTo('tag', {async: True}),
// });

// App.Directory.FIXTURES = [
// {
//     "id": "Images-49c47319-1387-48c4-aab7-381923f07f7c",
//     "parent": "#",
//     "title": "Images-49c47319-1387-48c4-aab7-381923f07f7c",
//     "icon": "/",
//     "root": true
// },
// {
//     "id": "objects",
//     "parent": "Images-49c47319-1387-48c4-aab7-381923f07f7c",
//     "title": "objects",
//     "icon": "/"
// },
// {
//     "id": "lion.svg",
//     "parent": "objects",
//     "title": "lion.svg",
//     "icon": "file",
//     "format": "fmt/91",
//     "size": "5"
// },
// {
//     "id": "799px-Euroleague-LE Roma vs Toulouse IC-27.bmp",
//     "parent": "objects",
//     "title": "799px-Euroleague-LE Roma vs Toulouse IC-27.bmp",
//     "icon": "file",
//     "format": "fmt/116",
//     "size": "1.3"
// },
// {
//     "id": "WFPC01.GIF",
//     "parent": "objects",
//     "title": "WFPC01.GIF",
//     "icon": "file",
//     "format": "fmt/4",
//     "size": "8"
// },
// {
//     "id": "Nemastylis_geminiflora_Flower.PNG",
//     "parent": "objects",
//     "title": "Nemastylis_geminiflora_Flower.PNG",
//     "icon": "file",
//     "format": "fmt/11",
//     "size": "13"
// },
// {
//     "id": "pictures",
//     "parent": "objects",
//     "title": "pictures",
//     "icon": "/"
// },
// {
//     "id": "MARBLES.TGA",
//     "parent": "pictures",
//     "title": "MARBLES.TGA",
//     "icon": "file",
//     "format": "fmt/402",
//     "size": "18"
// },
// {
//     "id": "Landing zone.jpg",
//     "parent": "pictures",
//     "title": "Landing zone.jpg",
//     "icon": "file",
//     "format": "fmt/43",
//     "size": "0.5"
// },
// {
//     "id": "Vector.NET-Free-Vector-Art-Pack-28-Freedom-Flight.eps",
//     "parent": "objects",
//     "title": "Vector.NET-Free-Vector-Art-Pack-28-Freedom-Flight.eps",
//     "icon": "file",
//     "format": "fmt/124",
//     "size": "0.1"
// },
// {
//     "id": "BBhelmet.ai",
//     "parent": "objects",
//     "title": "BBhelmet.ai",
//     "icon": "file",
//     "format": "fmt/19",
//     "size": "5"
// },
// {
//     "id": "G31DS.TIF",
//     "parent": "objects",
//     "title": "G31DS.TIF",
//     "icon": "file",
//     "foramt": "fmt/353",
//     "size": "15"
// },
// {
//     "id": "oakland03.jp2",
//     "parent": "objects",
//     "title": "oakland03.jp2",
//     "icon": "file",
//     "format": "x-fmt/392",
//     "size": "3.5"
// }
// ];
