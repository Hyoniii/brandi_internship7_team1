<template>
  <div id="ProductList">
    <a-layout-content
      :style="{
        background: '#fff',
        padding: '24px',
        margin: 0,
      }"
    >
     
      <div style="margin-bottom: 20px" class="selectBox">
      <div class="select_calendar">
        <span>조회기간</span><a-range-picker :size="size"  />
        </div>
       
        <div class="searchinfo">
          <div class="sellerName">
            <div class="nameDesc">셀러명</div><a-input class="margin" placeholder="검색어를 입력하세요." v-model="userName"/></a-input>
          </div>
        <div class="productOption">
          <div class="selectOption">
          <a-cascader
            :options="options"
            placeholder="Select"
            @change="onChange"/></div>
          <div class="searchProduct"><a-input
            placeholder="검색어를 입력하세요."
            v-model="userName"
          /></a-input></div>
        </div>
        </div>
        
        <div class="seller_status">
        <span>셀러속성</span>
        <div class="margin">
          <button class="btns" @click="handleBtnColor = !handleBtnColor" >전체</button>
          <button class="btns2" type="button">쇼핑몰</button>
          <button class="btns2" type="button">마켓</button>
          <button class="btns2" type="button">로드샵</button>
          <button class="btns2" type="button">디자이너브랜드</button>
          <button class="btns2" type="button">제너럴브랜드</button>
          <button class="btns2" type="button">네셔널브랜드</button>
          <button class="btns2" type="">뷰티</button></div>
        </div>
       
        <div class="sellingVisible">
        <div class="isSelling">
        <span>판매여부</span>
        <div class="margin">
          <button class="btns" type="button">전체</button>
          <button class="btns2" type="button">판매</button>
          <button class="btns2" type="button">미판매</button>
          </div>
        </div>
        <div class="isVisible">
        <span>진열여부</span>
        <div class="margin">
          <button class="btns" type="button">전체</button>
          <button class="btns2" type="button">진열</button>
          <button class="btns2" type="button">미진열</button>
        </div></div>
        </div>
       
        <div class="isDiscount">
        <span>할인여부</span>
          <div class="margin">
          <button class="btns" type="button">전체</button>
          <button class="btns2" type="button">할인</button>
          <button class="btns2" type="button">미할인</button>
        </div></div>

      <div class="submitbtns">
      <a-button class="submitBtn"type="primary" @search="onSearch">
      검색
    </a-button>
      <a-button class="resetBtn" slot="enterButton" @search="onSearch">
        초기화
      </a-button></div>
    

        
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
import moment from "moment";

const columns = [
  
  {
    title: "등록일",
    dataIndex: "created_at",
  },
  // {
  //   title: "대표이미지",
  //   //dataIndex: "desc_img_url",
  //   //render: desc_img_url => <img alt={desc_img_url} src={desc_img_url} />  // 'theImageURL' is the variable you must declare in order the render the URL
  // },
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
    dataIndex: "seller_status",
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
    dataIndex: "is_visible",
  },
  {
    title: "할인여부",
    dataIndex: "is_discount",
  },
];


export default {
  name: "productlist",
  components: {},
  data() {
    return {
      btnClicked: false,
      size: "default",
      data: [],
      columns,
      searchText: "",
      searchInput: null,
      searchedColumn: "",
      selectedProducts: [],
      userName: "",
      options: [
        {value: 'productName',
          label: '상품명'},
          {value: 'productCode',
          label: '상품명'},
          {value: 'productnumber',
          label: '상품번호'}]
    };
  },
  methods: {
    loadTableData() {
      const queryHeader = {
        headers: {
          AUTHORIZATION:
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjoxMzUsImV4cGlyYXRpb24iOiIyMDIwLTEyLTA3IDA1OjA0OjIxLjc3MjM0NyJ9.x02PwEcmCGJu2WxukGRgOfAxzVewiozgaYqtoH_rqD4",
        },
      };
      axios.get("http://10.251.1.163:5000/products").then((response) => {
        console.log(response);
        if (response.status === 200){
        const { product_list } = response.data;
        this.data = product_list;
        this.data.map((item, idx) => {
          this.data[idx].created_at = item.created_at.slice(0, 10)
          if (this.data[idx].discount_price == null){
            this.data[idx].discount_price = this.data[idx].price}
        })        
        
        }
      });
    },
    handleBtnColor(){
      this.btnClicked = !this.btnClicked;
    },
    onSearch(value) {
      console.log(value);
    },
    handleMenuClick(e) {
      console.log('click', e);},
    onChange(value) {
      console.log(value);
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
.selectBox{
  display:flex;
  height:280px;
  flex-direction: column; 
  justify-content: space-between;
}
.seller_status{
  width:80%;
  display:flex;
  

}
.btns, .btns2{
  width:100px;
  height:34px;
  text-align: center;
  line-height: 34px;
  border-radius:5px;
}
.btns{
  color:white;
  background:#3FAAFF;
}
.btns2 {
  color:#3FAAFF;
  background:white;
  border:solid 1px #3FAAFF;
}

.submitBtn, .resetBtn{
  width:100px;
}
.margin{
  margin-left:10px;
  display:inline-block;
}
.nameDesc {
  width:50px;
}
.sellerName {
  width: 300px;
}
.searchProduct{
  width: 250px;
}
.productOption, .sellerName, .isSelling .isVisible {
  display:flex;
}
.submitbtns{
   display:flex;
  justify-content:center;
  margin-top:30px;
}
.searchinfo, .sellingVisible{
  display:flex;
  width:80%;
  justify-content: space-between;
}

button { cursor:pointer; }
</style>
