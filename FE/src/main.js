import Vue from "vue";
import App from "./App";
import VueRouter from "vue-router";
import Routes from "./Routes";
import "ant-design-vue/dist/antd.css";
import Antd from "ant-design-vue";
import "../src/styles.scss";

Vue.use(Antd);
Vue.use(VueRouter);

const router = new VueRouter({
  routes: Routes,
  mode: "history",
  linkActiveClass: "active",
});

Vue.config.productionTip = false;

new Vue({
  el: "#app",
  router,
  components: { App },
  template: "<App/>",
});
