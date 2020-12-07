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
        <a-button type="primary" :disabled="!hasSelected" @click="start"
          >Reload</a-button
        >
        <span style="margin-left: 8px">
          <template v-if="hasSelected">{{
            `Selected ${selectedRowKeys.length} items`
          }}</template>
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
            >Search</a-button
          >
          <a-button
            size="small"
            style="width: 90px"
            @click="() => handleReset(clearFilters)"
            >Reset</a-button
          >
        </div>
        <a-icon
          slot="filterIcon"
          slot-scope="filtered"
          type="search"
          :style="{ color: filtered ? '#108ee9' : undefined }"
        />
        <template slot="email" slot-scope="text">
          <a :href="sellerDetailsLink" @click="handleSellerDetailsLink">
            {{ text }}
          </a>
        </template>
        <template slot="status" slot-scope="sellerStatus">
          <span :id="sellerStatus.id" :key="sellerStatus.id">
            {{ sellerStatus.name }}
          </span>
        </template>
        <template slot="sellerType" slot-scope="sellerType">
          <span :id="sellerType.id" :key="sellerType.id">
            {{ sellerType.name }}
          </span>
        </template>
        <span slot="actionButtons" slot-scope="actions">
          <a-tag
            v-for="action in actions"
            :key="action.id"
            :color="
              action.name === '입점 승인'
                ? 'blue'
                : action.name === '입점 거절' ||
                  action.name === '퇴점신청 처리' ||
                  action.name === '퇴점확정 처리'
                ? 'red'
                : action.name === '휴점 신청'
                ? 'yellow'
                : 'green'
            "
          >
            <a-button
              @click="confirmAction"
              :id="action.id"
              size="small"
              class="tableButtons"
              >{{ action.name }}</a-button
            >
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
                >{{ fragment }}</mark
              >
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

// f
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
      ageTarget: [
        { id: 1, value: "10대" },
        { id: 2, value: "20대초반" },
        { id: 3, value: "20대중반" },
        { id: 4, value: "20대후반" },
        { id: 5, value: "30대" },
        { id: 6, value: "연령대선택안함" },
      ],
      styleTarget: [
        { id: 1, value: "심플베이직" },
        { id: 2, value: "러블리" },
        { id: 3, value: "페미닌" },
        { id: 4, value: "캐주얼" },
        { id: 5, value: "섹시글램" },
        { id: 6, value: "스타일선택안함" },
      ],
      commissionFeesTarget: [
        { id: 1, type: "A안", value: "9%" },
        { id: 2, type: "C안", value: "9%" },
        { id: 3, type: "E안", value: "13%" },
      ],
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
          title: "셀러아이디",
          dataIndex: "email",
          key: "email",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "email",
          },
          fixed: "left",
          width: 170,
          sorter: true,
          onFilter: (value, record) =>
            record.email.toString().toLowerCase().includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: (visible) => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus();
              });
            }
          },
        },
        {
          title: "번호",
          dataIndex: "sellerNumber",
          key: "sellerNumber",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "customRender",
          },
          width: 130,
          sorter: true,
          onFilter: (value, record) =>
            record.sellerNumber
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
          title: "영문이름",
          dataIndex: "englishLabel",
          key: "englishLabel",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "customRender",
          },
          width: 100,
          onFilter: (value, record) =>
            record.englishLabel
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
          dataIndex: "koreanLabel",
          key: "koreanLabel",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "customRender",
          },
          width: 100,
          onFilter: (value, record) =>
            record.koreanLabel
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
          dataIndex: "repName",
          key: "repName",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "customRender",
          },
          width: 120,
          onFilter: (value, record) =>
            record.repName
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
          dataIndex: "sellerStatus",
          key: "sellerStatus",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "status",
          },
          width: 110,
          onFilter: (value, record) =>
            record.sellerStatus
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
          dataIndex: "repPhoneNumber",
          key: "repPhoneNumber",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "customRender",
          },
          width: 150,
          onFilter: (value, record) =>
            record.repPhoneNumber
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
          dataIndex: "repEmail",
          key: "repEmail",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "customRender",
          },
          width: 170,
          onFilter: (value, record) =>
            record.repEmail
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
          dataIndex: "sellerType",
          key: "sellerType",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "sellerType",
          },
          width: 110,
          onFilter: (value, record) =>
            record.sellerType
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
          dataIndex: "dateCreated",
          key: "dateCreated",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "customRender",
          },
          width: 180,
          sorter: true,
          onFilter: (value, record) =>
            record.dateCreated
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
          width: 350,
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
    confirmAction(e) {
      console.log(e.target.id);
      if (+e.target.id === 1) {
        this.sellerAccepted = true;
      }
      if (+e.target.id === 2) {
        this.$confirm({
          title: "Confirm",
          content: "셀러의 입점을 거절하시겠습니까?",
          onOk: () => {
            // disable 시키는법 구현중
            this.handleOk();
          },
        });
      }
      if (+e.target.id === 5) {
        this.$confirm({
          title: "Confirm",
          content:
            "퇴점 확정 시 셀러의 모든 상품이 미진열/미판매로 전환 되고 상품 관리를 할 수 없게 됩니다. 퇴점 확정을 하시겠습니까?",
          onOk: () => {
            // disable 시키는법 구현중
          },
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
    handleSellerDetailsLink() {},
    loadTableData() {
      axios.get("http://localhost:9000/static/seller_data.json").then((res) => {
        const { data } = res.data;
        this.data = data;
      });

      // seller_id: data.id,
      // join_date: data.dateCreated,
      // account_email: data.email,
      // seller_number: data.sellerNumber,
      // rep_name: data.repName,
      // rep_email: data.repEmail,
      // manager_phone: data.repPhoneNumber,
      // english_label: data.englishLabel,
      // korean_label: data.koreanLabel,
      // seller_status: data.sellerStatus.name,
      // seller_status_id: data.sellerStatus.id,
      // seller_type: data.sellerType,
      // service_number: data.repPhoneNumber,
      // seller_type: data.sellerType.name,
      // subcategory_id: data.sellerType.id,
      // account_id: data.accountTypeId,
      // is_active: data.isActive,
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
