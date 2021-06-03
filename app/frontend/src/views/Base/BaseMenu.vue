<template functional>
  <a-sub-menu :key="props.menuValue.key">
    <span slot="title">
      <a-icon v-if="props.menuValue.icon" :type="props.menuValue.icon" />
      <span>{{ props.menuValue.title }}</span>
    </span>
    <template v-for="(child, index) in props.menuValue.children">
      <a-menu-item v-if="!child.children.length" :key="index">
        <router-link :to="child.path">{{ child.title }}</router-link>
      </a-menu-item>
      <BaseMenu v-else :key="index" :menuValue="child"/>
    </template>
  </a-sub-menu>
</template>

<script>

import Vue from 'vue';
import { Icon, Menu } from 'ant-design-vue';

Vue.use(Menu);
Vue.use(Icon);

export default {
  name: 'BaseMenu',
  props: {
    menuValue: Object,
  },
  data() {
    return {

    };
  },
  created() {
    console.log('Key:', this.$props.subMenuKey);
    console.log(this.$props.menuValue);
  },
};
</script>

<style scoped>

</style>
