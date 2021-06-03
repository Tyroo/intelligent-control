<template>
  <a-layout
    id="components-layout-demo-custom-trigger"
    :style="{
      minHeight: layoutMinHeight
    }"
  >
    <a-layout-sider
      v-model="collapsed"
      :trigger="null"
      theme="light"
      collapsible
    >
      <div class="logo">
        <span class="logo-span">IECS</span>
      </div>
      <a-menu
        :default-selected-keys="[0]"
        :default-open-keys="['item_0']"
        :openKeys="openKeys"
        :selectedKeys="selectedKeys"
        mode="inline"
        @openChange="handleOpen"
        @click="handleClick"
        :style="{ minHeight: menuMinHeight }"
      >
        <template v-for="item in menuValue">
          <a-menu-item v-if="!item.children.length" :key="item.key">
            <a-icon :type="item.icon" />
            <router-link :to="item.path">{{ item.title }}</router-link>
          </a-menu-item>
          <BaseMenu :menuValue="item" :key="item.key"/>
        </template>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header style="background: #fff; padding: 0">
        <a-icon
            class="trigger"
            :type="collapsed ? 'menu-unfold' : 'menu-fold'"
            @click="() => (collapsed = !collapsed)"
        />
        <a-icon class="logout" type="logout" @click="logout"/>
      </a-layout-header>
      <a-layout-content
        :style="{
        margin: '16px',
        padding: '24px',
        background: '#fff',
        }"
      >
        <router-view></router-view>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script>
import Vue from 'vue';
import { Layout, Menu, Icon } from 'ant-design-vue';
import { clickUserLogout } from '@/api/api';
import BaseMenu from './BaseMenu';

Vue.use(Layout);
Vue.use(Menu);
Vue.use(Icon);

export default {
  name: 'BaseContainer',
  components: { BaseMenu },
  data() {
    const layoutMinHeight = `${window.innerHeight}px`;
    const menuMinHeight = `${window.innerHeight - 64}px`;

    return {
      defaultPagePath: '/IntelligentLighting',
      openKeys: [],
      selectedKeys: [0],
      collapsed: false,
      layoutMinHeight,
      menuMinHeight,
      menuValue: [],
      menuSelectValue: [],
    };
  },
  created() {
    this.createMenu();
    this.getCurrentSelectMenu();
  },
  methods: {
    logout() {
      clickUserLogout({ token: localStorage.getItem('x-token') });
    },
    handleOpen(value) {
      this.openKeys = value;
    },
    handleClick(value) {
      this.selectedKeys.pop();
      this.selectedKeys.push(value.key);
    },
    recursionMenuValue(items) {
      const obj = {};
      if (items.meta.icon) {
        obj.icon = items.meta.icon;
      }
      obj.title = items.meta.title;
      obj.children = [];
      obj.path = items.path || '';

      if (items.children) {
        items.children.map((item) => {
          if (!item.hidden) {
            obj.children.push(this.recursionMenuValue(item));
          }
        });
      }
      return obj;
    },

    createMenu() {
      const menuList = this.$router.options.routes;
      menuList.forEach((items) => {
        if (items.hidden) return;
        this.menuValue.push(this.recursionMenuValue(items));
      });
    },

    getCurrentSelectMenu() {
      const { path } = this.$router.currentRoute;
      const pathArray = [];

      let index = 0;
      while (index !== -1) {
        index = path.indexOf('/', index + 1);
        if (index > 0) {
          pathArray.push(path.substring(0, index));
        }
      }
      pathArray.push(path);

      if (pathArray[0] === this.defaultPagePath) {
        pathArray[0] = '/';
      }
      this.recursionSelectMenu(this.menuValue, pathArray);

      const msvEnd = this.menuSelectValue.pop();
      const msv = [];

      this.menuSelectValue.map((item) => {
        msv.push(`item_${item}`);
      });
      this.openKeys = msv;
      this.selectedKeys = [msvEnd];
    },

    recursionSelectMenu(menuObj, cArr) {
      let indexValue = 0;
      let menuValue = [];

      menuObj.some((value, index) => {
        indexValue = cArr.indexOf(value.path) + 1;

        if (indexValue > 0) {
          this.menuSelectValue.push(index);
          menuValue = value.children;
          return true;
        }
      });
      if (indexValue > 0 && indexValue < cArr.length + 1) {
        this.recursionSelectMenu(menuValue, cArr);
      }
    },
  },
};
</script>

<style lang="less" scoped>
#components-layout-demo-custom-trigger {
  box-sizing: border-box;
  .trigger {
    font-size: 18px;
    line-height: 64px;
    padding: 0 24px;
    cursor: pointer;
    transition: color 0.3s;
    float: left;
  }
  .logo {
    height: 64px;
    background: rgba(255, 255, 255, 0.2);
    border-right: solid 1px #e8e8e8;
    .logo-span {
      font-weight: bold;
      color: white;
      line-height: 64px;
      font-family: 琥珀体;
      font-size: 28px;
      margin: 0;
      background: #1b6eeaa8;
      border-radius: 10px;
    }
  }
  .logout {
    line-height: 64px;
    cursor: pointer;
    font-size: 18px;
    width: 64px;
    float: right;
  }
}

.trigger:hover {
  color: #1890ff;
}

.logout:hover {
  color: #1890ff;
}

</style>
