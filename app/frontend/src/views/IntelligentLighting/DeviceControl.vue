<template xmlns:a-col="http://www.w3.org/1999/html">
  <a-spin tip="L o a d i n g" size="large" :spinning="spinning">
    <a-row>
      <a-row :gutter="[0,{ xs: 8, sm: 16, md: 24}]">
        <a-col>
          <div class="title-card">
            <a-icon type="control" theme="filled" :style="{ color: '#1890ff', fontSize: '24px' }"/>
            <span class="title">设备控制</span>
          </div>
        </a-col>
      </a-row>
      <a-row :gutter="[0,{ xs: 8, sm: 16, md: 24}]">
        <a-col span="8">
          <a-card
            title="设备亮度"
            :style="{width: '100%', height: '100%', borderRadius: '20px'}"
            :headStyle="{ color: '#aaa', fontWeight: 'bold' }"
          >
            <span :style="{ fontSize: '30px', color: '#1890ff', fontWeight: 'bold'}">
              {{`${Number(formData.deviceStatus) && formData.lightIntensity*20}%`}}
            </span>
          </a-card>
        </a-col>
        <a-col span="8" :style="{ display: 'flex', justifyContent: 'center' }">
          <LightBulb :status="formData.deviceStatus"/>
        </a-col>
        <a-col span="8">
          <a-card
            title="环境亮度"
            :style="{width: '100%', height: '100%', borderRadius: '20px'}"
            :headStyle="{ color: '#aaa', fontWeight: 'bold' }"
          >
            <span :style="{ fontSize: '30px', color: '#1890ff', fontWeight: 'bold'}">
              {{`${lightAmbient*20}%`}}
            </span>
          </a-card>
        </a-col>
      </a-row>
      <a-row :gutter="[0,{ xs: 8, sm: 16, md: 24}]">
        <a-col :style="{ display: 'flex', alignItems: 'center', justifyContent: 'center' }">
          <a-button type="primary" @click="onRefreshPage">
            刷新
          </a-button>
        </a-col>
      </a-row>
      <a-row :gutter="[0,{ xs: 8, sm: 16, md: 24}]" type="flex" align="middle">
        <a-col span="12">
          <a-form :form="form">
            <a-form-item
              label="设备状态"
              :labelCol="{span: 4, offset: 0}"
              :wrapperCol="{span: 16, offset: 0}"
            >
              <a-switch
                v-decorator="['deviceStatus', { valuePropName: 'checked' }]"
                checked-children="开"
                un-checked-children="关"
                @click="onEquipmentStatusControl"
              />
            </a-form-item>
            <a-form-item
                label="控制模式"
                :labelCol="{span: 4, offset: 0}"
                :wrapperCol="{span: 16, offset: 0}"
            >
              <a-radio-group v-decorator="['controlModel']">
                <a-radio :value="0">
                  自动模式
                </a-radio>
                <a-radio :value="1">
                  手动模式
                </a-radio>
              </a-radio-group>
            </a-form-item>
            <a-form-item
                label="通信模式"
                :labelCol="{span: 4, offset: 0}"
                :wrapperCol="{span: 16, offset: 0}"
            >
              <a-radio-group v-decorator="['communicationMode']">
                <a-radio :value="0">
                  透传模式
                </a-radio>
                <a-radio :value="1">
                  监听模式
                </a-radio>
                <a-radio :value="2">
                  休眠模式
                </a-radio>
              </a-radio-group>
            </a-form-item>
            <a-form-item
              label="设备亮度"
              :labelCol="{span: 4, offset: 0}"
              :wrapperCol="{span: 14, offset: 0}"
            >
              <a-slider
                  v-decorator="['lightIntensity']"
                  :marks="{ 1: '弱', 2: '较弱', 3: '中', 4: '较强', 5: '强' }"
                  :min="1"
                  :max="5"
                  :step="1"
                  :dots="true"
              />
            </a-form-item>
          </a-form>
        </a-col>
        <a-col span="12">
          <a-table
            :columns="columns"
            :data-source="data"
            :bordered="true"
            :pagination="false"
          >
            <span slot="image" slot-scope="text, record">
              <img :style="{ height: '80px' }" :src="record.image" />
            </span>
          </a-table>
        </a-col>
      </a-row>
      <a-row>
        <a-col>
          <a-button
            type="primary"
            @click="onSaveSetting"
          >
            保存设置
          </a-button>
        </a-col>
      </a-row>
    </a-row>
  </a-spin>
</template>

<script>
import Vue from 'vue';
import {
  Icon, Row, Col, Card, Button, Form,
  Switch, Slider, Radio, Table, message,
  Modal, Spin,
} from 'ant-design-vue';
import LightBulb from '@/views/IntelligentLighting/LightBulb';

import { deviceStatusChange, getDeviceAllStatus } from '@/api/api';

Vue.use(Icon);
Vue.use(Row);
Vue.use(Col);
Vue.use(Card);
Vue.use(Button);
Vue.use(Form);
Vue.use(Switch);
Vue.use(Slider);
Vue.use(Radio);
Vue.use(Table);
Vue.use(message);
Vue.use(Modal);
Vue.use(Spin);

// eslint-disable-next-line no-unused-vars
const columns = [
  {
    title: '设备型号',
    align: 'center',
    dataIndex: 'model',
    key: 'model',
  },
  {
    title: '设备图片',
    align: 'center',
    dataIndex: 'image',
    key: 'image',
    scopedSlots: { customRender: 'image' },
  },
];

const data = [
  {
    key: '1',
    model: 'ILD001',
    image: require('../../assets/led.jpg'),
  },
];

export default {
  name: 'EquipmentControl',
  components: {
    LightBulb,
  },
  data() {
    return {
      // 显示数据定义
      spinning: false,
      data,
      columns,
      lightAmbient: 3,
      formData: {
        deviceStatus: true,
        controlModel: 0,
        communicationMode: 0,
        lightIntensity: 3,
      },
    };
  },
  beforeCreate() {
    // 创建form表单对象
    this.form = this.$form.createForm(this);
  },
  created() {
    this.updatePageAllData();
  },
  methods: {
    // 更新整个页面的数据
    updatePageAllData() {
      this.spinning = true;
      getDeviceAllStatus({ params: 1 })
        .then((res) => {
          this.spinning = false;
          // eslint-disable-next-line no-shadow
          const { data } = res.data;
          this.formData = {
            deviceStatus: !!((data.charAt(0) - 0)),
            controlModel: (data.charAt(1) - 0),
            communicationMode: (data.charAt(2) - 0),
            lightIntensity: (data.charAt(3) - 0),
          };
          this.lightAmbient = (data.charAt(4) - 0);
          this.$nextTick(() => this.form.setFieldsValue(this.formData));
          this.deviceStatus = !this.formData.deviceStatus;
        })
        .catch((err) => {
          this.spinning = false;
          this.$nextTick(() => this.form.setFieldsValue(this.formData));
          this.deviceStatus = !this.formData.deviceStatus;
          console.log(err.data.statusText);
        });
    },

    // 设备状态更改触发
    onEquipmentStatusControl(checked) {
      this.deviceStatus = !checked;
    },

    // 点击保存按钮触发
    // eslint-disable-next-line consistent-return
    onSaveSetting() {
      const fieldsValue = this.form.getFieldsValue();
      const v1 = JSON.stringify(fieldsValue);
      const v2 = JSON.stringify(this.formData);

      if (v1 === v2) {
        message.info('未更改设置');
        return false;
      }
      if (!this.formData.controlModel) {
        fieldsValue.controlModel = 1;
      }

      this.form.setFieldsValue(fieldsValue);
      this.formData = fieldsValue;
      fieldsValue.deviceStatus = fieldsValue.deviceStatus ? 1 : 0;

      deviceStatusChange(fieldsValue);
      message.success('更改成功');
    },

    // 点击刷新按钮触发
    onRefreshPage() {
      this.updatePageAllData();
    },
  },
};
</script>

<style lang="less" scoped>
.title-card {
  border-bottom: solid 2px #eee;
  text-align: left;
}

.title {
  margin-left: 10px;
  color: #1890ff;
  font-size: 24px;
  font-weight: bold;
}

/deep/ .ant-form-item-control {
  text-align: left;
  margin-left: 10px;
}

/deep/ .ant-form-item-label label{
  color: #aaa;
  font-size: 18px;
  font-weight: bold;
}

//.form-item {
//  display: block;
//  text-align: left;
//}
</style>
