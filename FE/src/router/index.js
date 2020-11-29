import Vue from "vue";
import Router from "vue-router";
import Login from "../Pages/Login/Login.vue";
import Signup from "../Pages/Signup/Signup.vue";
import Main from "../Pages/Main/Main.vue";
import SellerList from "../Pages/SellerList/SellerList.vue";

Vue.use(Router);
export default new Router({
  mode: "history",
  routes: [
    {
      path: "/",
      component: Login,
    },
    {
      path: "/signup",
      component: Signup,
    },
    {
      path: "/:menu",
      component: Main,
      children: [
        {
          path: "sellerlist",
          component: SellerList,
        },
      ],
    },
  ],
});
