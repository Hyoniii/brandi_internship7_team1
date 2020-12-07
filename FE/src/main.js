import Vue from "vue";
import App from "./App";
import VueRouter from "vue-router";
import Routes from "./Routes";
import "ant-design-vue/dist/antd.css";
import Antd from "ant-design-vue";
import "../src/styles.scss";
import axios from "axios";

Vue.use(Antd);
Vue.use(VueRouter);

axios.defaults.headers.common["AUTHORIZATION"] =
  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjoxMjcsImV4cGlyYXRpb24iOiIyMDIwLTEyLTAyIDA2OjA5OjIwLjIzNTU0OCJ9.wug1dOSu9ZjcQXN5xwp35kAtr-N1wrDX0P7D7d2r9bo";

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
