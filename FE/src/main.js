import Vue from 'vue'
import App from './App'
import router from './router'
import 'ant-design-vue/dist/antd.css';
import Antd from 'ant-design-vue';
import "../src/styles.scss";

Vue.use(Antd);
Vue.config.productionTip = false;

new Vue({
    el: '#app',
    router,
    components: { App },
    template: '<App/>'
})