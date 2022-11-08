import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import './assets/global.css'
import request from "./utils/request";
import request1 from "./utils/request1";
import store from './store'

Vue.config.productionTip = false

Vue.use(ElementUI, {size: "mini"});

Vue.prototype.request = request
Vue.prototype.request1 = request1

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')