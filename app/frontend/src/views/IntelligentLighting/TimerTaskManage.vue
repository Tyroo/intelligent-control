<template>
  <a-spin tip="L o a d i n g" size="large" :spinning="spinning">
    <a-row>
      <a-row :gutter="[0,{ xs: 8, sm: 16, md: 24}]">
        <a-col>
          <div class="title-card">
            <a-icon type="clock-circle" :style="{ color: '#1890ff', fontSize: '24px' }"/>
            <span class="title">定时任务</span>
          </div>
        </a-col>
      </a-row>
      <a-row>
        <a-row>
          <a-col span="24" :style="{ display: 'flex', justifyContent: 'flex-end', AlignItems: 'center', height: '60px' }">
            <div>
              <a-button type="primary" @click="addTimerWork">
                新增任务
              </a-button>
              <a-modal
                v-model="visible"
                :title="editorOrAdd? '新增定时任务':'编辑定时任务'"
                ok-text="保存"
                cancel-text="取消"
                @ok="submitTimerWorkData"
              >
                <a-form
                    id="components-form-demo-validate-other"
                    :form="form"
                    v-bind="formItemLayout"
                >
                  <a-form-item label="任务编号">
                    <a-input
                      v-decorator="['WorkNumber', { initialValue: '' }]"
                      type="text"
                      disabled
                      placeholder="此项由系统自动生成"
                    >
                    </a-input>
                  </a-form-item>
                  <a-form-item label="任务内容">
                    <a-textarea
                      v-decorator="['WorkContent', { initialValue: '' }]"
                      type="text"
                      placeholder="描述一下任务的大概作用..."
                    >
                    </a-textarea>
                  </a-form-item>
                  <a-form-item label="设备状态">
                    <a-switch
                      v-decorator="['DeviceStatus',
                        { valuePropName: 'checked', initialValue: true }
                      ]"
                      checked-children="开"
                      un-checked-children="关"
                    >
                    </a-switch>
                  </a-form-item>
                  <a-form-item label="设备亮度" has-feedback>
                    <a-select
                     v-decorator="
                     ['DeviceBrightness',
                       {
                         rules: [{ required: true, message: '请选择设备亮度' }],
                       },
                     ]"
                     placeholder="请选择设备亮度"
                    >
                      <a-select-option v-for="(value, key) in [20,40,60,80,100]" :value="value" :key="key">
                        {{value}}
                      </a-select-option>
                    </a-select>
                  </a-form-item>
                  <a-form-item label="时间规则" has-feedback>
                    <a-input
                      v-decorator="
                      ['TimeRules',
                        {
                          initialValue: '',
                          rules:
                          [{
                            required: true,
                            validator: timeRulesValidator,
                          }],
                        },
                      ]"
                      type="text"
                      placeholder="格式：[Y,m,d,H,M,S]"
                    >
                    </a-input>
                  </a-form-item>
                  <a-form-item label="创建时间">
                    <a-input
                      v-decorator="['CreateTime', { initialValue: '' }]"
                      type="text"
                      disabled
                      placeholder="此项由系统自动生成"
                    >
                    </a-input>
                  </a-form-item>
                </a-form>
              </a-modal>
            </div>
          </a-col>
        </a-row>
        <a-row>
          <a-col span="24" :style="{ display: 'flex', justifyContent: 'center' }">
            <a-table
              :columns="columns"
              :data-source="tableData"
              :style="{ flex: 1, height: '600px' }"
              :defaultPageSize="5"
            >
              <template slot="Operation" slot-scope="text, record">
                <div class="table-operation" >
                  <span @click="deleteTimerWork(record.key)">删除</span>
                  <span @click="editorTimerWork(record.key)">编辑</span>
                </div>
              </template>

              <div slot="DeviceStatus" slot-scope="value">
                <span :style="{ color: value? 'Lime':'red', fontSize: '26px' }">●</span>
              </div>
            </a-table>
          </a-col>
        </a-row>
      </a-row>
    </a-row>
  </a-spin>
</template>

<script>
import Vue from 'vue';
import {
  Icon, Row, Col, Card, Button, Form,
  Switch, Slider, Radio, Table, message,
  Modal, Spin, Input, Select,
} from 'ant-design-vue';

import { compareObjectsValues, timeRangeValidator } from '@/utils/tools';
import { getTimerWorkQueues, changeTimerWorkTerms, deleteTimerWorkTerms } from '@/api/api';

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
Vue.use(Input);
Vue.use(Select);

const columns = [
  {
    title: '任务编号',
    align: 'center',
    dataIndex: 'WorkNumber',
  },
  {
    title: '任务内容',
    align: 'center',
    dataIndex: 'WorkContent',
  },
  {
    title: '设备状态',
    align: 'center',
    dataIndex: 'DeviceStatus',
    scopedSlots: { customRender: 'DeviceStatus' },
  },
  {
    title: '设备亮度',
    align: 'center',
    dataIndex: 'DeviceBrightness',
  },
  {
    title: '时间规则',
    align: 'center',
    dataIndex: 'TimeRules',
  },
  {
    title: '创建时间',
    align: 'center',
    dataIndex: 'CreateTime',
  },
  {
    title: '操作',
    align: 'center',
    dataIndex: 'Operation',
    scopedSlots: { customRender: 'Operation' },
  },
];

export default {
  name: 'TimerTaskManage',
  data() {
    return {
      editorOrAdd: true, // true为新增，false为编辑
      spinning: false,
      tableData: [
      //     {
      //   key: 0,
      //   WorkNumber: 0,
      //   WorkContent: '每天6:00开启设备',
      //   DeviceStatus: true,
      //   DeviceBrightness: 80,
      //   TimeRules: '[*,*,*,6,0,0]',
      //   CreateTime: '2021-04-28 16:21:24',
      // }
      ],
      editorKey: -1,
      columns,
      visible: false,
      formItemLayout: {
        labelCol: { span: 6 },
        wrapperCol: { span: 14 },
      },
    };
  },
  beforeCreate() {
    this.form = this.$form.createForm(this, { name: 'validate_other' });
  },
  created() {
    this.getTimerWork();
  },
  methods: {
    // 时间规则表单项验证函数
    timeRulesValidator(rule, value, mFn) {
      const reg = /^\[(\d{4}|\*),(\d{1,2}|\*|\d+\-\d+),(\d{1,2}|\*|\d+\-\d+),(\d{1,2}|\*|\d+\-\d+),(\d{1,2}|\*|\d+\-\d+),(\d{1,2}|\*|\d+\-\d+),(\d{1}|\*|\d+\-\d+)\]$/;
      if (!value) {
        mFn('请输入时间规则');
      } else if (!reg.test(value)) {
        mFn('时间格式不正确');
      } else if (!timeRangeValidator(value)) {
        mFn('时间超出范围');
      } else {
        mFn();
      }
    },
    // 获取定时任务
    getTimerWork() {
      this.spinning = false;
      getTimerWorkQueues({ params: 'timer_work_queues' })
        .then((res) => {
          const { data } = res.data;
          this.tableData = data;
          this.spinning = false;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    // 新增定时任务
    addTimerWork() {
      this.editorOrAdd = true;
      this.form.resetFields();
      this.visible = true;
    },

    findTableTermValue(termKey) {
      const termValue = this.tableData.filter((data) => data.key === termKey)[0] || {};

      const newTermValue = Object.assign({}, termValue);

      this.editorKey = newTermValue.key;
      delete newTermValue.key;

      if (!termValue.WorkNumber) return [-1, newTermValue];
      return [this.tableData.indexOf(termValue), newTermValue];
    },

    editorTimerWork(key) {
      const [termIndex, termValue] = this.findTableTermValue(key);
      this.editorOrAdd = false;

      if (termIndex === -1) {
        return message.info('请刷新页面后重试');
      }
      this.visible = true;
      this.$nextTick(() => {
        this.form.setFieldsValue(termValue);
      });
    },

    deleteTimerWork(key) {
      const [termIndex, termValue] = this.findTableTermValue(key);

      if (termIndex === -1) {
        return message.info('请刷新页面后重试');
      }
      this.tableData.splice(termIndex, 1);
      deleteTimerWorkTerms({ delete_key: termValue.WorkNumber })
        .then((res) => {
          this.getTimerWork();
        })
        .catch((err) => {
          console.log(err);
        });
    },

    submitTimerWorkData(e) {
      e.preventDefault();
      this.form.validateFields((err, values) => {
        if (!err) {
          this.visible = false;
          if (values.WorkNumber) {
            // 编辑
            const newData = [...this.tableData];
            const [termIndex, termValue] = this.findTableTermValue(this.editorKey);
            const changeFlag = compareObjectsValues(termValue, values);

            if (changeFlag) {
              message.info('未改变定时任务值');
              return;
            }
            Object.assign(newData[termIndex], values);
            this.tableData = newData;
          } else {
            // 新增
            const date = new Date();
            values.key = date.getTime();
            this.tableData.push({ ...values });
          }
          // pass 发送post请求
          changeTimerWorkTerms({ ...values });
          message.success('请手动刷新页面');
          console.log('success: ', values);
        } else {
          console.log('error: ', values);
        }
      });
    },
  },
  computed: {

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

/deep/ .ant-table-column-title {
  font-weight: bold;
  font-size: 16px;
}

.table-operation {
  > span {
    color: #1890ff;
    margin: 0 5px;
    cursor: pointer;

  }
}
#components-form-demo-validate-other .dropbox {
  height: 180px;
  line-height: 1.5;
}
</style>
