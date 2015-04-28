// import Ember from 'ember';
// import config from './config/environment';

// var Router = Ember.Router.extend({
//   location: config.locationType
// });

// export default Router.map(function() {
// });

App.Router.map(function () {
  this.resource('arrange', { path: '/' });
});

App.ArrangeRoute = Ember.Route.extend({
    model: function () {
        return this.store.find('directory');
    }
});
