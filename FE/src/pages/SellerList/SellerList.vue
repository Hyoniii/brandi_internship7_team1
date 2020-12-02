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
        <a-button
          type="primary"
          :disabled="!hasSelected"
          :loading="loading"
          @click="start"
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
        <template slot="sellerId" slot-scope="text">
          <a :href="sellerDetailsLink" @click="handleSellerDetailsLink">
            {{ text }}
          </a>
          <!-- <router-link to="/foo" tag="button">foo</router-link> -->
        </template>
        <span slot="actionButtons" slot-scope="actions">
          <a-tag
            class="actionBtn"
            v-for="action in actions"
            :key="action"
            v-model="actionButton"
            :color="
              action === '입점승인' || action === '휴점신청'
                ? 'blue'
                : action === '입점거절' ||
                  action === '퇴점신청처리' ||
                  action === '퇴점확정처리'
                ? 'red'
                : action === '휴점신청'
                ? 'yellow'
                : 'green'
            "
          >
            <a-button class="tableButtons">{{ action }}</a-button>
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
import VueTableDynamic from "vue-table-dynamic";
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
    actions: ["입점승인", "입점거절"],
    tags: ["nice", "developer"],
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
    actions: ["입점거절", "퇴점신청처리"],
    tags: ["loser"],
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
    actions: ["입점승인", "퇴점확정처리", "퇴점철회처리"],
    tags: ["cool", "teacher"],
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
    actions: ["휴점신청", "휴점해제"],
    tags: ["cool", "teacher"],
  },
  {
    id: "5",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "퇴점대기",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: ["퇴점철회처리", "휴점신청"],
    tags: ["cool", "teacher"],
  },
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
    actions: ["입점승인", "입점거절"],
    tags: ["nice", "developer"],
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
    actions: ["입점거절", "퇴점신청처리"],
    tags: ["loser"],
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
    actions: ["입점승인", "퇴점확정처리", "퇴점철회처리"],
    tags: ["cool", "teacher"],
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
    actions: ["휴점신청", "휴점해제"],
    tags: ["cool", "teacher"],
  },
  {
    id: "5",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "퇴점대기",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: ["퇴점철회처리", "휴점신청"],
    tags: ["cool", "teacher"],
  },
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
    actions: ["입점승인", "입점거절"],
    tags: ["nice", "developer"],
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
    actions: ["입점거절", "퇴점신청처리"],
    tags: ["loser"],
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
    actions: ["입점승인", "퇴점확정처리", "퇴점철회처리"],
    tags: ["cool", "teacher"],
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
    actions: ["휴점신청", "휴점해제"],
    tags: ["cool", "teacher"],
  },
  {
    id: "5",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "퇴점대기",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: ["퇴점철회처리", "휴점신청"],
    tags: ["cool", "teacher"],
  },
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
    actions: ["입점승인", "입점거절"],
    tags: ["nice", "developer"],
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
    actions: ["입점거절", "퇴점신청처리"],
    tags: ["loser"],
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
    actions: ["입점승인", "퇴점확정처리", "퇴점철회처리"],
    tags: ["cool", "teacher"],
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
    actions: ["휴점신청", "휴점해제"],
    tags: ["cool", "teacher"],
  },
  {
    id: "5",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "퇴점대기",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: ["퇴점철회처리", "휴점신청"],
    tags: ["cool", "teacher"],
  },
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
    actions: ["입점승인", "입점거절"],
    tags: ["nice", "developer"],
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
    actions: ["입점거절", "퇴점신청처리"],
    tags: ["loser"],
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
    actions: ["입점승인", "퇴점확정처리", "퇴점철회처리"],
    tags: ["cool", "teacher"],
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
    actions: ["휴점신청", "휴점해제"],
    tags: ["cool", "teacher"],
  },
  {
    id: "5",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "퇴점대기",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: ["퇴점철회처리", "휴점신청"],
    tags: ["cool", "teacher"],
  },
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
    actions: ["입점승인", "입점거절"],
    tags: ["nice", "developer"],
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
    actions: ["입점거절", "퇴점신청처리"],
    tags: ["loser"],
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
    actions: ["입점승인", "퇴점확정처리", "퇴점철회처리"],
    tags: ["cool", "teacher"],
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
    actions: ["휴점신청", "휴점해제"],
    tags: ["cool", "teacher"],
  },
  {
    id: "5",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "퇴점대기",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: ["퇴점철회처리", "휴점신청"],
    tags: ["cool", "teacher"],
  },
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
    actions: ["입점승인", "입점거절"],
    tags: ["nice", "developer"],
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
    actions: ["입점거절", "퇴점신청처리"],
    tags: ["loser"],
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
    actions: ["입점승인", "퇴점확정처리", "퇴점철회처리"],
    tags: ["cool", "teacher"],
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
    actions: ["휴점신청", "휴점해제"],
    tags: ["cool", "teacher"],
  },
  {
    id: "5",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "퇴점대기",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: ["퇴점철회처리", "휴점신청"],
    tags: ["cool", "teacher"],
  },
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
    actions: ["입점승인", "입점거절"],
    tags: ["nice", "developer"],
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
    actions: ["입점거절", "퇴점신청처리"],
    tags: ["loser"],
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
    actions: ["입점승인", "퇴점확정처리", "퇴점철회처리"],
    tags: ["cool", "teacher"],
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
    actions: ["휴점신청", "휴점해제"],
    tags: ["cool", "teacher"],
  },
  {
    id: "5",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "퇴점대기",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: ["퇴점철회처리", "휴점신청"],
    tags: ["cool", "teacher"],
  },
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
    actions: ["입점승인", "입점거절"],
    tags: ["nice", "developer"],
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
    actions: ["입점거절", "퇴점신청처리"],
    tags: ["loser"],
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
    actions: ["입점승인", "퇴점확정처리", "퇴점철회처리"],
    tags: ["cool", "teacher"],
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
    actions: ["휴점신청", "휴점해제"],
    tags: ["cool", "teacher"],
  },
  {
    id: "5",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "퇴점대기",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: ["퇴점철회처리", "휴점신청"],
    tags: ["cool", "teacher"],
  },
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
    actions: ["입점승인", "입점거절"],
    tags: ["nice", "developer"],
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
    actions: ["입점거절", "퇴점신청처리"],
    tags: ["loser"],
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
    actions: ["입점승인", "퇴점확정처리", "퇴점철회처리"],
    tags: ["cool", "teacher"],
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
    actions: ["휴점신청", "휴점해제"],
    tags: ["cool", "teacher"],
  },
  {
    id: "5",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "퇴점대기",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: ["퇴점철회처리", "휴점신청"],
    tags: ["cool", "teacher"],
  },
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
    actions: ["입점승인", "입점거절"],
    tags: ["nice", "developer"],
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
    actions: ["입점거절", "퇴점신청처리"],
    tags: ["loser"],
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
    actions: ["입점승인", "퇴점확정처리", "퇴점철회처리"],
    tags: ["cool", "teacher"],
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
    actions: ["휴점신청", "휴점해제"],
    tags: ["cool", "teacher"],
  },
  {
    id: "5",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "퇴점대기",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: ["퇴점철회처리", "휴점신청"],
    tags: ["cool", "teacher"],
  },
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
    actions: ["입점승인", "입점거절"],
    tags: ["nice", "developer"],
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
    actions: ["입점거절", "퇴점신청처리"],
    tags: ["loser"],
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
    actions: ["입점승인", "퇴점확정처리", "퇴점철회처리"],
    tags: ["cool", "teacher"],
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
    actions: ["휴점신청", "휴점해제"],
    tags: ["cool", "teacher"],
  },
  {
    id: "5",
    sellerNumber: "2398402983",
    name: "fsjdkf",
    englishLabel: "shelby",
    koreanLabel: "김보보",
    repName: "담당자2",
    sellerStatus: "퇴점대기",
    repPhoneNumber: "010-4021-4932",
    repEmail: "nblasfd@gmail.com",
    sellerType: "쇼핑몰",
    dateCreated: "	2020-11-27 16:56:37",
    actions: ["퇴점철회처리", "휴점신청"],
    tags: ["cool", "teacher"],
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
      actionButton: "",
      sellerDetailsLink: "https://www.brandi.co.kr/",
      searchText: "",
      searchInput: null,
      searchedColumn: "",
      selectedRowKeys: [],
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
          width: 370,
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
      this.loading = true;
      // ajax request after empty completing
      setTimeout(() => {
        this.loading = false;
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

#SellerList {
}
</style>
