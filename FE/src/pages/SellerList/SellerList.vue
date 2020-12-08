<template>
  <div id="SellerList">
    <a-layout-content
      class="sellerListBody"
      :style="{
        background: '#fff',
        padding: '24px',
        margin: 0,
      }"
    >
      <div style="margin-bottom: 14px">
        <a-button type="primary" :disabled="!hasSelected" @click="start">Reload</a-button>
        <span style="margin-left: 8px">
          <template v-if="hasSelected">
            {{
            `Selected ${selectedRowKeys.length} items`
            }}
          </template>
        </span>
      </div>
      <a-table
        :scroll="{ x: 1300 }"
        :pagination="pagination"
        :data-source="data"
        :columns="columns"
        :row-selection="{
          selectedRowKeys: selectedRowKeys,
          onChange: onSelectChange,
        }"
      >
        <div
          slot="filterDropdown"
          slot-scope="{
            setSelectedKeys,
            selectedKeys,
            confirm,
            clearFilters,
            column,
          }"
          style="padding: 8px"
        >
          <a-input
            v-ant-ref="(c) => (searchInput = c)"
            :placeholder="`Search ${column.dataIndex}`"
            :value="selectedKeys[0]"
            style="width: 188px; margin-bottom: 8px; display: block"
            @change="
              (e) => setSelectedKeys(e.target.value ? [e.target.value] : [])
            "
            @pressEnter="
              () => handleSearch(selectedKeys, confirm, column.dataIndex)
            "
          />
          <a-button
            type="primary"
            icon="search"
            size="small"
            style="width: 90px; margin-right: 8px"
            @click="() => handleSearch(selectedKeys, confirm, column.dataIndex)"
          >Search</a-button>
          <a-button size="small" style="width: 90px" @click="() => handleReset(clearFilters)">Reset</a-button>
        </div>
        <a-icon
          slot="filterIcon"
          slot-scope="filtered"
          type="search"
          :style="{ color: filtered ? '#108ee9' : undefined }"
        />
        <!-- ================= data row ==================  -->
        <template slot="account_email" slot-scope="text">
          <a :href="sellerDetailsLink" @click="handleSellerDetailsLink">{{ text }}</a>
        </template>
        <template slot="status" slot-scope="text">
          <span :id="seller_status_id" :key="seller_status_id">{{ text }}</span>
        </template>
        <template slot="sellertype" slot-scope="text">
          <span :id="subcategory_id" :key="subcategory_id">{{ text }}</span>
        </template>
        <span slot="actionButtons" slot-scope="actions">
          <a-tag
            v-for="action in actions"
            :key="action.action_id"
            @click="handleColorChange"
            :color="
              action.action_name === '입점 승인'
                ? 'blue'
                : action.action_name === '입점 거절' ||
                  action.action_name === '퇴점신청 처리' ||
                  action.action_name === '퇴점확정 처리'
                ? 'red'
                : action.action_name === '휴점 신청'
                ? 'yellow'
                : 'green'
            "
          >
            <a-button
              @click="confirmAction"
              :id="action.action_id"
              :name="action.status_id"
              :data-seller="action.seller_id"
              size="small"
              class="tableButtons"
            >{{ action.action_name }}</a-button>
          </a-tag>
        </span>
        <template slot="customRender" slot-scope="text, record, index, column">
          <span v-if="searchText && searchedColumn === column.dataIndex">
            <template
              v-for="(fragment, i) in text
                .toString()
                .split(new RegExp(`(?<=${searchText})|(?=${searchText})`, 'i'))"
            >
              <mark
                v-if="fragment.toLowerCase() === searchText.toLowerCase()"
                :key="i"
                class="highlight"
              >{{ fragment }}</mark>
              <template v-else>{{ fragment }}</template>
            </template>
          </span>
          <template v-else>{{ text }}</template>
        </template>
      </a-table>
    </a-layout-content>
  </div>
</template>

<script>
import axios from "axios";
import MainHeader from "../../Components/MainHeader";

const sellerListAPI = "http://192.168.7.21:5000/account/seller_list";
const actionStatusAPI =
  "http://192.168.7.21:5000/account/change_seller_status";

export default {
  name: "sellerlist",
  components: {
    "main-header": MainHeader,
  },
  data() {
    return {
      data: [],
      sellerDetailsLink: "https://www.brandi.co.kr/",
      searchText: "",
      searchInput: null,
      searchedColumn: "",
      selectedRowKeys: [],
      sellerAccepted: false,
      sellerAcceptedBtnLoading: false,
      pagination: {
        defaultCurrent: 1, // Default current page number
        defaultPageSize: 10, // The default size of the data displayed on the current page
        total: 0, // total number, must first
        showSizeChanger: true,
        showQuickJumper: true,
        pageSizeOptions: ["5", "10", "20", "50", "100"],
        showTotal: (total) => `Total ${total} items`, // Show total
        onShowSizeChange: (current, pageSize) => {
          this.pagination.defaultCurrent = 1;
          this.pagination.defaultPageSize = pageSize;
        },
        // Update the display when changing the number per page
        onChange: (current, size) => {
          this.pagination.defaultCurrent = current;
          this.pagination.defaultPageSize = size;
        },
      },
      columns: [
        {
          title: "번호",
          dataIndex: "account_id",
          key: "account_id",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "customRender",
          },
          width: 100,
          onFilter: (value, record) =>
            record.account_id
              .toString()
              .toLowerCase()
              .includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: (visible) => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus();
              }, 0);
            }
          },
        },
        {
          title: "셀러아이디",
          dataIndex: "account_email",
          key: "account_email",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "account_email",
          },
          width: 170,
          onFilter: (value, record) =>
            record.account_email
              .toString()
              .toLowerCase()
              .includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: (visible) => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus();
              });
            }
          },
        },
        {
          title: "영문이름",
          dataIndex: "english_label",
          key: "english_label",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "customRender",
          },
          width: 120,
          onFilter: (value, record) =>
            record.english_label
              .toString()
              .toLowerCase()
              .includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: (visible) => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus();
              });
            }
          },
        },
        {
          title: "한글이름",
          dataIndex: "korean_label",
          key: "korean_label",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "customRender",
          },
          width: 120,
          onFilter: (value, record) =>
            record.korean_label
              .toString()
              .toLowerCase()
              .includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: (visible) => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus();
              });
            }
          },
        },
        {
          title: "담당자이름",
          dataIndex: "manager_name",
          key: "manager_name",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "customRender",
          },
          width: 120,
          onFilter: (value, record) =>
            record.manager_name
              .toString()
              .toLowerCase()
              .includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: (visible) => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus();
              });
            }
          },
        },
        {
          title: "셀러상태",
          dataIndex: "seller_status",
          key: "seller_status_id",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "status",
          },
          width: 120,
          onFilter: (value, record) =>
            record.seller_status
              .toString()
              .toLowerCase()
              .includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: (visible) => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus();
              });
            }
          },
        },
        {
          title: "담당자연락처",
          dataIndex: "manager_phone",
          key: "manager_phone",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "customRender",
          },
          width: 120,
          onFilter: (value, record) =>
            record.manager_phone
              .toString()
              .toLowerCase()
              .includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: (visible) => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus();
              });
            }
          },
        },
        {
          title: "담당자이메일",
          dataIndex: "manager_email",
          key: "manager_email",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "customRender",
          },
          width: 140,
          onFilter: (value, record) =>
            record.manager_email
              .toString()
              .toLowerCase()
              .includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: (visible) => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus();
              });
            }
          },
        },
        {
          title: "셀러속성",
          dataIndex: "subcategory_name",
          key: "subcategory_id",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "sellertype",
          },
          width: 120,
          onFilter: (value, record) =>
            record.subcategory_name
              .toString()
              .toLowerCase()
              .includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: (visible) => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus();
              });
            }
          },
        },
        {
          title: "등록일시",
          dataIndex: "join_date",
          key: "join_date",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "customRender",
          },
          width: 160,
          sorter: true,
          onFilter: (value, record) =>
            record.join_date
              .toString()
              .toLowerCase()
              .includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: (visible) => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus();
              });
            }
          },
        },
        {
          title: "Actions",
          dataIndex: "actions",
          key: "actions",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "actionButtons",
          },
          fixed: "right",
          width: 300,
          onFilter: (value, record) =>
            record.actions
              .toString()
              .toLowerCase()
              .includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: (visible) => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus();
              });
            }
          },
        },
      ],
    };
  },
  methods: {
    postQuery(action, status, seller) {
      const queryBody = {
        seller_id: seller,
        action_id: action,
        status_id: status,
      };

      const queryHeader = {
        headers: {
          AUTHORIZATION:
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjoxMjcsImV4cGlyYXRpb24iOiIyMDIwLTEyLTAyIDA2OjA5OjIwLjIzNTU0OCJ9.wug1dOSu9ZjcQXN5xwp35kAtr-N1wrDX0P7D7d2r9bo",
        },
      };

      axios.post(actionStatusAPI, queryBody, queryHeader).then((res) => {
        if (res.status === 200) return alert("성공");
      });
    },

    confirmAction(e) {
      console.log(e.target.dataset.seller, "sdfkljskdfjlsdf");
      const { id, name } = e.target;
      const { seller } = e.target.dataset;

      //입점승인
      console.log(id, name, seller);
      if (id == 1) {
        this.$confirm({
          title: "Confirm",
          content: "셀러의 입점을 승인하시겠습니까?",
          onOk: () => {
            this.handleOk();
            this.postQuery(id, name, seller);
            this.loadTableData();
          },
        });
      }
      //입점거절
      if (+id === 2) {
        this.$confirm({
          title: "Confirm",
          content: "셀러의 입점을 거절하시겠습니까?",
          onOk: () => {
            this.handleOk();
          },
        });
      }
      //휴점 신청
      if (+id === 3) {
        this.$confirm({
          title: "Confirm",
          content:
            "휴점처리 시 셀러의 모든 상품이 미진열/미판매로 전환 되고 상품 관리를 할 수 없게 됩니다. 휴점신청을 하시겠습니까?",
          onOk: () => {
            this.handleOk();
          },
        });
      }
      //퇴점신청 처리
      if (+id === 4) {
        this.$confirm({
          title: "Confirm",
          content:
            "퇴점신청 시 셀러의 모든 상품이 미진열/미판매로 전환 되고 상품 관리를 할 수 없게 됩니다. 퇴점신청을 하시겠습니까?",
          onOk: () => {
            this.handleOk();
          },
        });
      }
      //휴점해제
      if (+id === 7) {
        this.$confirm({
          title: "Confirm",
          content:
            "휴점해제 시 셀러의 모든 상품이 진열/판매로 전환 되고 상품 관리를 할 수 있습니다. 휴점해제를 하시겠습니까?",
          onOk: () => {
            this.handleOk();
          },
        });
      }
      //퇴점확정 처리
      if (+id === 5) {
        this.$confirm({
          title: "Confirm",
          content:
            "퇴점 확정 시 셀러의 모든 상품이 미진열/미판매로 전환 되고 상품 관리를 할 수 없게 됩니다. 퇴점 확정을 하시겠습니까?",
          onOk: () => {},
        });
      }
      //퇴점철회 처리
      if (+id === 6) {
        this.$confirm({
          title: "Confirm",
          content:
            "퇴점철회 시 셀러의 모든 상품이 진열/판매로 전화 되고 상품 관리를 할 수 있습니다. 퇴점철회를 하시겠습니까?",
          onOk: () => {},
        });
      }
    },
    handleOk(e) {
      this.sellerAcceptedBtnLoading = true;
      setTimeout(() => {
        this.sellerAccepted = false;
        this.sellerAcceptedBtnLoading = false;
      }, 3000);
    },
    handleCancel(e) {
      this.sellerAccepted = false;
    },
    handleSearch(selectedKeys, confirm, dataIndex) {
      confirm();
      this.searchText = selectedKeys[0];
      this.searchedColumn = dataIndex;
    },
    handleReset(clearFilters) {
      clearFilters();
      this.searchText = "";
    },
    start() {
      // ajax request after empty completing
      setTimeout(() => {
        this.selectedRowKeys = [];
      }, 1000);
    },
    onSelectChange(selectedRowKeys) {
      console.log("selectedRowKeys changed: ", selectedRowKeys);
      this.selectedRowKeys = selectedRowKeys;
    },
    handleSellerDetailsLink() {
      
    },

    loadTableData() {
      const queryHeader = {
        headers: {
          AUTHORIZATION:
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjoxMjcsImV4cGlyYXRpb24iOiIyMDIwLTEyLTAyIDA2OjA5OjIwLjIzNTU0OCJ9.wug1dOSu9ZjcQXN5xwp35kAtr-N1wrDX0P7D7d2r9bo",
        },
      };

      axios.get(sellerListAPI, queryHeader).then((res) => {
        const { seller_list } = res.data;
        seller_list.forEach((info) => {
          info.actions.forEach((action) => {
            action["seller_id"] = info.seller_id;
          });
        });
        this.data = seller_list;
      });
    },
  },
  computed: {
    hasSelected() {
      return this.selectedRowKeys.length > 0;
    },
  },

  mounted() {
    this.loadTableData();
  },
};
</script>

<style lang="scss">
@import "../../styles.scss";
</style>
