<template>
  <div id="ProductList">
    <a-layout-content
      :style="{
        // background: '#fff',
        padding: '24px',
        margin: 0,
      }"
    >
      <div style="margin-bottom: 14px">
        <a-button type="primary">Primary</a-button>
        <a-input
          ref="userNameInput"
          v-model="userName"
          placeholder="Basic usage"
        >
          <a-icon slot="prefix" type="user" />
          <a-tooltip slot="suffix" title="Extra information">
            <a-icon type="info-circle" style="color: rgba(0, 0, 0, 0.45)" />
          </a-tooltip>
        </a-input>
      </div>
      <a-table
        :row-selection="rowSelection"
        :columns="columns"
        :data-source="data"
        :scroll="{ x: 1300 }"
      >
        <a slot="name" slot-scope="text">{{ text }}</a>
      </a-table>
    </a-layout-content>
  </div>
</template>

<script>
import axios from "axios";

const columns = [
  {
    title: "등록상태",
    dataIndex: "name",
    scopedSlots: { customRender: "name" },
  },
  {
    title: "등록일",
    dataIndex: "product_code",
  },
  {
    title: "대표이미지",
    dataIndex: "",
  },
  {
    title: "상품명",
    dataIndex: "product_name",
  },
  {
    title: "상품코드",
    dataIndex: "product_code",
  },
  {
    title: "상품번호",
    dataIndex: "product_id",
  },
  {
    title: "셀러속성",
    dataIndex: "",
  },
  {
    title: "셀러명",
    dataIndex: "seller_name",
  },
  {
    title: "판매가",
    dataIndex: "price",
  },
  {
    title: "할인가",
    dataIndex: "discount_price",
  },
  {
    title: "판매여부",
    dataIndex: "is_selling",
  },
  {
    title: "진열여부",
    dataIndex: "",
  },
  {
    title: "할인여부",
    dataIndex: "",
  },
  {
    title: "Actions",
    dataIndex: "",
  },
];
const data = [
  {
    account_id: 2,
    created_at: "2020-12-06 15:49:31",
    desc_img_url:
      "https://brandi-intern01.s3.ap-northeast-2.amazonaws.com/product_image_1",
    discount_price: null,
    is_discount: 0,
    is_selling: 1,
    is_visible: 1,
    number: "4571",
    price: 218000,
    product_code: "9BF5A4",
    product_id: 457,
    product_name: "점퍼",
    seller_name: "브랜디샵",
    seller_status: "입점",
    seller_subcategory_name: "쇼핑몰",
  },
  {
    account_id: 2,
    created_at: "2020-12-06 15:42:56",
    desc_img_url:
      "https://brandi-intern.s3.ap-northeast-2.amazonaws.com/product_image_1",
    discount_price: null,
    is_discount: 0,
    is_selling: 1,
    is_visible: 1,
    number: "4561",
    price: 218000,
    product_code: "A0E0C5",
    product_id: 456,
    product_name: "오트밀 롱코트 ",
    seller_name: "브랜디샵",
    seller_status: "입점",
    seller_subcategory_name: "쇼핑몰",
  },
  {
    account_id: 1,
    created_at: "2020-12-06 15:41:38",
    desc_img_url:
      "https://brandi-intern.s3.ap-northeast-2.amazonaws.com/product_image_1",
    discount_price: null,
    is_discount: 0,
    is_selling: 1,
    is_visible: 1,
    number: "4551",
    price: 120000,
    product_code: "F17E52",
    product_id: 455,
    product_name: "퍼자켓",
    seller_name: "제너럴브랜드샵",
    seller_status: "퇴점",
    seller_subcategory_name: "제너럴브랜드",
  },
];

export default {
  name: "productlist",
  components: {},
  data() {
    return {
      data: [],
      columns,
      searchText: "",
      searchInput: null,
      searchedColumn: "",
      selectedProducts: [],
      userName: "",
    };
  },
  method: {
    loadTableData() {
      // axios
      //   .get("http://localhost:9000/static/product_data.json")
      //   .then((res) => {
      //     const { product_list } = res.data;
      //     this.data = product_list;
      //   });
    },
  },
  computed: {
    rowSelection() {
      return {
        onChange: (selectedRowKeys, selectedRows) => {
          console.log(
            `selectedRowKeys: ${selectedRowKeys}`,
            "selectedRows: ",
            selectedRows
          );
          this.selectedProducts = selectedRows;
        },
      };
    },
  },
  mounted() {},
};
</script>

<style lang="css">
@import "../../styles.scss";
</style>
