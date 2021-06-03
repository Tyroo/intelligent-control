<template>
  <a-layout
    id="components-layout-demo-custom-trigger"
    :style="{
      minHeight: layoutMinHeight,
      background: '#1b2b41',
      opacity: 0.8,
    }"
  >
    <a-layout-content
    :style="{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      flexDirection: 'column',
    }">
      <a-card :style="{ background: 'transparent' }" :bordered="false">
        <a-row>
          <a-col>
            <div class="system-title">
              <span class="system-name">智能设备控制系统</span>
              <span class="system_icon">IECS</span>
            </div>
          </a-col>
        </a-row>
      </a-card>
      <a-card
        hoverable
        size="small"
        class="login-card"
      >
        <a-row type="flex" justify="center" align="middle" :style="{ marginTop: '70px' }">
          <a-col span="10">
            <a-form  :form="form">
              <a-form-item>
                <a-input
                    v-decorator="['username', { initialValue: '', rules: [{ required: true, message: '请输入账号' }]}]"
                    type="text"
                    placeholder="用户名"
                >
                </a-input>
              </a-form-item>
              <a-form-item>
                <a-input
                    v-decorator="['password', { initialValue: '', rules: [{ required: true, message: '请输入密码' }]}]"
                    type="password"
                    placeholder="密码"
                >
                </a-input>
              </a-form-item>
              <a-button
                @click="submitLoginInfo"
              >登录
              </a-button>
            </a-form>
          </a-col>
        </a-row>
      </a-card>
    </a-layout-content>
  </a-layout>
</template>

<script>

import Vue from 'vue';
import {
  Card, Row, Col, Form,
  Button, Input, Layout,
} from 'ant-design-vue';

import { clickUserLogin } from '@/api/api';
import { localgetItem } from '@/request/localstory';

Vue.use(Card);
Vue.use(Row);
Vue.use(Col);
Vue.use(Form);
Vue.use(Button);
Vue.use(Input);
Vue.use(Layout);

export default {
  name: 'Login',
  data() {
    const layoutMinHeight = `${window.innerHeight}px`;
    return {
      layoutMinHeight,
    };
  },
  beforeCreate() {
    // 创建form表单对象
    this.form = this.$form.createForm(this);
  },
  methods: {
    submitLoginInfo() {
      this.form.validateFields((err, values) => {
        if (!err) {
          clickUserLogin(values)
            .then((res) => {
              const { data } = res;
              const token = data['x-token'];

              if (token) {
                localStorage.setItem('x-token', token);
                this.$router.push('/IntelligentLighting/DeviceControl');
              }
            })
            .catch((error) => {
              console.log(error.statusText);
            });
        }
      });
    },
  },
};
</script>

<style lang="less" scoped>
.system-title {
  .system-name {
    color: #1890ff;
    font-weight: bold;
    font-size: 30px;
    user-select: none;
  }
  .system_icon {
    display: inline-block;
    color: white;
    background: red;
    border-radius: 25px;
    font-size: 16px;
    vertical-align: top;
    padding: 0 2px;
    user-select: none;
  }
}
  .login-card {
    width: 55%;
    background: transparent;
    border: solid 2px #1890ff;
    height: 300px;
    margin: 0 auto;
    border-radius: 10px;
  }

  .login-card:hover{
    border: none;
  }

  .ant-input {
    border-width: 3px;
  }

  .login {
    color: red;
  }
</style>
