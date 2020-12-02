<template>
  <div id="Main">
    <main-top-nav />

    <a-layout class="mainContainer">
      <main-side-nav />

      <a-layout style="padding: 24px" class="routerViewContainer">
        <a-page-header
          :v-if="this.$route.path == '/main'"
          style="border: 1px solid rgb(235, 237, 240)"
          title="Title"
          :breadcrumb="{ props: { routes } }"
          sub-title="This is a
        subtitle"
        />
        <router-view />
      </a-layout>
    </a-layout>
    <main-footer />
  </div>
</template>

<script>
import MainTopNav from "../../Components/MainTopNav";
import MainSideNav from "../../Components/MainSideNav";
import MainFooter from "../../Components/MainFooter";
import SellerList from "../SellerList/SellerList";
export default {
  name: "main",

  components: {
    "main-top-nav": MainTopNav,
    "main-footer": MainFooter,
    "main-side-nav": MainSideNav,
    "seller-list": SellerList,
  },
  data() {
    return {
      routes: [
        {
          path: "index",
          breadcrumbName: "First-level Menu",
        },
        {
          path: "first",
          breadcrumbName: "Second-level Menu",
        },
        {
          path: "second",
          breadcrumbName: "Third-level Menu",
        },
      ],
    };
  },
  created() {
    // this.$route.path; // /teams/t1
    // console.log(this.$route);
    const menu = this.$route.params.menu;
  },
};
</script>

<style lang="scss">
@import "../../styles.scss";

#Main {
  display: flex;
  flex-direction: column;
  height: 100vh;

  .mainContainer {
    display: flex;
    height: 100vh;
    font-size: 13px;

    .routerViewContainer {
      .routerView {
      }
    }
  }
}
</style>
