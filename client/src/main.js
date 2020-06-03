import 'bootstrap/dist/css/bootstrap.css';
import BootstrapVue from 'bootstrap-vue';
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import moment from 'moment';
// imoprt { store } from './store/store'

Vue.use(BootstrapVue);

Vue.config.productionTip = false;

Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).utc().format('MMM Do h:mma')
  }
});

Vue.filter('formatTodayDate', function(value) {
  if (value) {
    return moment(String(value)).utc().format('h:mm a')
  }
});

new Vue({
  // store: store,
  router,
  render: h => h(App),
}).$mount('#app');

// import store from './store'
// import Axios from 'axios'
//
// Vue.prototype.$http = Axios;
// const token = localStorage.getItem('token')
// if (token) {
//   Vue.prototype.$http.defaults.headers.common['Authorization'] = token
// }
