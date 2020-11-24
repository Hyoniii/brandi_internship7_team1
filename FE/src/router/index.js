import Vue from 'vue'
import Router from 'vue-router'
import Login from '../pages/login/login.vue'
import Signup from '../pages/signup/signup.vue'
import SellerList from '../pages/sellerList/sellerList.vue'

Vue.use(Router)
export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            component: Login,
        },
        {
            path: '/signup',
            component: Signup,
        },
        {
            path: '/sellerList',
            component: SellerList,
        }

    ]
})