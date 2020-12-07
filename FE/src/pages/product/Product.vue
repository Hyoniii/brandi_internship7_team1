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
        <a-button type="primary" :disabled="!hasSelected"  @click="start">Reload</a-button>
        <span style="margin-left: 8px">
          <template v-if="hasSelected">{{ `Selected ${selectedRowKeys.length} items` }}</template>
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
        <template slot="sellerId" slot-scope="text">
          <a :href="sellerDetailsLink" @click="handleSellerDetailsLink">
            {{
            text
            }}
          </a>
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
            >{{ action.name }}</a-button>
          </a-tag>
          <a-modal v-model="sellerAccepted" title="셀러 태그 / 수수료 선택" on-ok="handleOk">
            <template slot="footer">
              <a-button key="back" @click="handleCancel">닫기</a-button>
              <a-button key="submit" type="primary"  @click="handleOk">입점 승인</a-button>
            </template>
            <div class="sellerAcceptForm">
              <a-form-item label="연령 선택">
                <a-radio-group v-decorator="['radio-group']" required>
                  <a-radio v-for="age in ageTarget" :value="age.id" :key="age.id">{{ age.value }}</a-radio>
                </a-radio-group>
              </a-form-item>
              <a-form-item label="스타일 선택" has-feedback>
                <a-select
                  v-decorator="
                    'select',
                    {
                      rules: [
                        {
                          required: true,
                          message: '스타일을 선택해주세요!',
                        },
                      ],
                    },
                  ]"
                  placeholder="스타일 선택"
                >
                  <a-select-option
                    v-for="style in styleTarget"
                    :value="style.id"
                    :key="style.id"
                  >{{ style.value }}</a-select-option>
                </a-select>
              </a-form-item>
              <a-form-item label="수수료">
                <a-radio-group v-decorator="['radio-button']">
                  <a-radio-button v-for="fee in commissionFeesTarget" :value="fee.id" :key="fee.id">
                    <span class="commissionFeeType">{{ fee.type }}:</span>
                    수수료 {{ fee.value }}
                  </a-radio-button>
                </a-radio-group>
              </a-form-item>
            </div>
          </a-modal>
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
import MainHeader from "../../Components/MainHeader";

const data = [
  {
    id: "1",
    sellerNumber: "22417",
    name: "gw111",
    englishLabel: "gyuwon",
    koreanLabel: "규상점",
    repName: "담당자",
    sellerStatus: "입점대기",
    repPhoneNumber: "010-1111-1234",
    repEmail: "email@email.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: [
      {
        id: 1,
        name: "입점 승인",
      },
      {
        id: 2,
        name: "입점 거절",
      },
    ],
  },
  {
    id: "2",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "입점",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: [
      {
        id: 3,
        name: "휴점 신청",
      },
      {
        id: 4,
        name: "퇴점신청 처리",
      },
    ],
  },
  {
    id: "3",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "휴점",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: [
      {
        id: 7,
        name: "휴점 해제",
      },
      {
        id: 4,
        name: "퇴점신청 처리",
      },
    ],
  },
  {
    id: "4",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "휴점",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: [
      {
        id: 3,
        name: "휴점 신청",
      },
      {
        id: 5,
        name: "퇴점확정 처리",
      },
      {
        id: 6,
        name: "퇴점철회 처리",
      },
    ],
  },
  {
    id: "5",
    sellerNumber: "22417",
    name: "gw111",
    englishLabel: "gyuwon",
    koreanLabel: "규상점",
    repName: "담당자",
    sellerStatus: "입점대기",
    repPhoneNumber: "010-1111-1234",
    repEmail: "email@email.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: [
      {
        id: 1,
        name: "입점 승인",
      },
      {
        id: 2,
        name: "입점 거절",
      },
    ],
  },
  {
    id: "6",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "입점",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: [
      {
        id: 3,
        name: "휴점 신청",
      },
      {
        id: 4,
        name: "퇴점신청 처리",
      },
    ],
  },
  {
    id: "7",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "휴점",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: [
      {
        id: 7,
        name: "휴점 해제",
      },
      {
        id: 4,
        name: "퇴점신청 처리",
      },
    ],
  },
  {
    id: "8",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "휴점",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: [
      {
        id: 3,
        name: "휴점 신청",
      },
      {
        id: 5,
        name: "퇴점확정 처리",
      },
      {
        id: 6,
        name: "퇴점철회 처리",
      },
    ],
  },
  {
    id: "9",
    sellerNumber: "22417",
    name: "gw111",
    englishLabel: "gyuwon",
    koreanLabel: "규상점",
    repName: "담당자",
    sellerStatus: "입점대기",
    repPhoneNumber: "010-1111-1234",
    repEmail: "email@email.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: [
      {
        id: 1,
        name: "입점 승인",
      },
      {
        id: 2,
        name: "입점 거절",
      },
    ],
  },
  {
    id: "10",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "입점",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: [
      {
        id: 3,
        name: "휴점 신청",
      },
      {
        id: 4,
        name: "퇴점신청 처리",
      },
    ],
  },
  {
    id: "11",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "휴점",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: [
      {
        id: 7,
        name: "휴점 해제",
      },
      {
        id: 4,
        name: "퇴점신청 처리",
      },
    ],
  },
  {
    id: "12",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "휴점",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: [
      {
        id: 3,
        name: "휴점 신청",
      },
      {
        id: 5,
        name: "퇴점확정 처리",
      },
      {
        id: 6,
        name: "퇴점철회 처리",
      },
    ],
  },
  {
    id: "13",
    sellerNumber: "22417",
    name: "gw111",
    englishLabel: "gyuwon",
    koreanLabel: "규상점",
    repName: "담당자",
    sellerStatus: "입점대기",
    repPhoneNumber: "010-1111-1234",
    repEmail: "email@email.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: [
      {
        id: 1,
        name: "입점 승인",
      },
      {
        id: 2,
        name: "입점 거절",
      },
    ],
  },
  {
    id: "14",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "입점",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: [
      {
        id: 3,
        name: "휴점 신청",
      },
      {
        id: 4,
        name: "퇴점신청 처리",
      },
    ],
  },
  {
    id: "15",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "휴점",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: [
      {
        id: 7,
        name: "휴점 해제",
      },
      {
        id: 4,
        name: "퇴점신청 처리",
      },
    ],
  },
  {
    id: "16",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "휴점",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: [
      {
        id: 3,
        name: "휴점 신청",
      },
      {
        id: 5,
        name: "퇴점확정 처리",
      },
      {
        id: 6,
        name: "퇴점철회 처리",
      },
    ],
  },
];

export default {
  name: "sellerlist",
  components: {
    "main-header": MainHeader,
  },
  data() {
    return {
      data,
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
          dataIndex: "name",
          key: "sellerId",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "sellerId",
          },
          fixed: "left",
          width: 140,
          sorter: true,
          onFilter: (value, record) =>
            record.sellerId
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
            customRender: "customRender",
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
            customRender: "customRender",
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
  },
  computed: {
    hasSelected() {
      return this.selectedRowKeys.length > 0;
    },
  },
  mounted() {
    // this.fetch();
  },
};
</script>

<style lang="scss">
@import "../../styles.scss";

</style>
