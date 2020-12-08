<template>
  <div id="OrderList">
    <a-layout-content
      :style="{
        background: '#fff',
        padding: '24px',
        margin: 0,
      }"
    >
      <div style="margin-bottom: 14px"></div>
      <a-table
        :row-selection="rowSelection"
        :columns="columns"
        :data-source="data"
        :scroll="{ x: 2000 }"
      >
        <a slot="name" slot-scope="text">{{ text }}</a>
      </a-table>
    </a-layout-content>
  </div>
</template>

<script>
import axios from 'axios';

const columns = [
  {
    title: "등록상태",
    dataIndex: "name",
    scopedSlots: { customRender: "name" },
  },
  {
    title: "등록일",
    dataIndex: "created_at",
  },
  {
    title: "대표이미지",
    dataIndex: "",
  },
  {
    title: "상품명",
    dataIndex: "",
  },
  {
    title: "상품코드",
    dataIndex: "",
  },
  {
    title: "상품번호",
    dataIndex: "",
  },
  {
    title: "셀러속성",
    dataIndex: "",
  },
  {
    title: "셀러명",
    dataIndex: "",
  },
  {
    title: "판매가",
    dataIndex: "",
  },
  {
    title: "할인가",
    dataIndex: "",
  },
  {
    title: "판매여부",
    dataIndex: "",
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
    buyer_name: "1팀",
    delivery_address_1: "제주도",
    delivery_address_2: "제주시",
    delivery_instruction: "경비실에 맡겨주세요",
    delivery_zip_code: "12345",
    detailed_order_number: "20201130000000012",
    discount_rate: null,
    id: 3,
    item_subtotal: 12000,
    option_color: null,
    option_size: null,
    order_number: "2020113000000001",
    order_quantity: 1,
    order_status: "배송중",
    order_status_id: 3,
    phone_number: "01012345678",
    product_name: "댄싱슈즈",
    product_number: "1741",
    product_price: 12000,
    purchase_date: "2020-11-29 15:08:07",
    seller_id: 1,
    seller_name_kr: "브랜디샵",
    total_order_amount: 42000,
    updated_at: "2020-12-07 21:29:59",
  },
  {
    buyer_name: "1팀",
    delivery_address_1: "제주도",
    delivery_address_2: "제주시",
    delivery_instruction: "경비실에 맡겨주세요",
    delivery_zip_code: "12345",
    detailed_order_number: "20201202000000031",
    discount_rate: null,
    id: 6,
    item_subtotal: 218000,
    option_color: "Black",
    option_size: "Free",
    order_number: "2020120200000003",
    order_quantity: 1,
    order_status: "배송중",
    order_status_id: 3,
    phone_number: "01012345678",
    product_name: "오트밀 롱코트 ",
    product_number: "4561",
    product_price: 218000,
    purchase_date: "2020-12-02 09:00:13",
    seller_id: 1,
    seller_name_kr: "브랜디샵",
    total_order_amount: 228000,
    updated_at: "2020-12-07 10:47:20",
  },
];
export default {
  name: "orderlist",
  components: {},
  data() {
    return {
      data: [],
      columns,
      searchText: "",
      searchInput: null,
      searchedColumn: "",
      selectedProducts: [],
    };
  },
  method: {
    loadTableData() {
      axios.get("http://localhost:9000/static/order_data.json").then((res) => {
        const { order_list } = res.data;
        this.data = order_list;
      });
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
  mounted() {
    this.loadTableData();
  },
};
</script>

<style lang="css">
@import "../../styles.scss";
</style>
