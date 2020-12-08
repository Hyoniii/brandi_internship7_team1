import Login from "./Pages/Login/Login.vue";
import Signup from "./Pages/Signup/Signup.vue";
import Main from "./Pages/Main/Main.vue";
import SellerList from "./Pages/SellerList/SellerList.vue";
import OrderList from "./Pages/OrderList/OrderList.vue";
import ProductList from "./Pages/ProductList/ProductList.vue";
import Home from "./Pages/Home/Home.vue";

// Vue.use(Router);

export default [
  {
    path: "/",
    name: "login",
    component: Login,
  },
  {
    path: "/signup",
    name: "signup",
    component: Signup,
  },
  {
    path: "/:menu",
    name: "mainpage",
    component: Main,
    children: [
      {
        path: "home",
        name: "home",
        component: Home,
      },
      {
        path: "sellerlist",
        name: "sellerlist",
        component: SellerList,
      },
      {
        path: "orderlist",
        name: "orderlist",
        component: OrderList,
      },
      {
        path: "productlist",
        name: "productlist",
        component: ProductList,
      },
    ],
  },
];
