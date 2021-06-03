<template>
  <a-spin tip="L o a d i n g" size="large" :spinning="spinning">
    <a-row>
      <a-row :gutter="[0,{ xs: 8, sm: 16, md: 24}]">
        <a-col>
          <div class="title-card">
            <a-icon type="pie-chart" :style="{ color: '#1890ff', fontSize: '24px' }"/>
            <span class="title">数据分析</span>
          </div>
        </a-col>
      </a-row>
      <a-row>
        <a-col span="24" :style="{ display: 'flex', justifyContent: 'center' }">
          <div v-if="dataList.length" ref="durationStatisticsChart" :style="{ flex: 1, height: '600px' }"></div>
          <a-empty v-else />
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
  Modal, Spin, Empty,
} from 'ant-design-vue';

import * as echarts from 'echarts/core';
import {
  TitleComponent,
  ToolboxComponent,
  DatasetComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
} from 'echarts/components';

import {
  BarChart,
  PieChart,
} from 'echarts/charts';
import {
  CanvasRenderer,
} from 'echarts/renderers';

import { getWeekUseDuration } from '@/api/api';

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
Vue.use(Empty);

echarts.use(
  [DatasetComponent, ToolboxComponent, TooltipComponent, TitleComponent, GridComponent, LegendComponent, BarChart, PieChart, CanvasRenderer],
);

export default {
  name: 'DataAnalysis',
  data() {
    return {
      spinning: false,
      dayList: [],
      dataList: [],
      option: {
        title: {
          text: '设备用时统计(近七天)',
          left: 'center',
          bottom: 'bottom',
        },
        tooltip: {
          trigger: 'axis',
          showContent: false,
        },
        legend: {
          top: '48%',
          left: 'center',
          data: ['2021-04-28', '2021-04-27', '2021-04-26', '2021-04-25', '2021-04-24', '2021-04-23', '2021-04-22'],
        },
        dataset: {
          source: [
            ['product', '2021-04-28', '2021-04-27', '2021-04-26', '2021-04-25', '2021-04-24', '2021-04-23', '2021-04-22'],
            ['duration', 1, 2, 3, 4, 3, 2, 2],
          ],
        },
        xAxis: {
          type: 'category',
          axisTick: {
            show: false,
          },
        },
        yAxis: {
          gridIndex: 0,
          axisLabel: {
            formatter: '{value}（分钟）',
          },
        },
        grid: { top: '60%' },
        series: [
          {
            type: 'bar',
            seriesLayoutBy: 'row',
            showBackground: true,
            barMaxWidth: '30%',
            backgroundStyle: {
              color: 'rgba(180, 180, 180, 0.2)',
            },
            itemStyle: {
              normal: {
                color(params) {
                  // 注意，如果颜色太少的话，后面颜色不会自动循环，最好多定义几个颜色
                  const colorList = ['#ee6666', '#fac858', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'];
                  return colorList[params.dataIndex];
                },
                label: {
                  show: true,
                  position: 'top',
                  textStyle: {
                    color: '#666',
                    fontSize: 13,
                  },
                },
              },
            },
          },
          {
            type: 'pie',
            seriesLayoutBy: 'row',
            id: 'pie',
            radius: '30%',
            center: ['50%', '20%'],
            emphasis: { focus: 'data' },
            label: {
              // formatter: '{b}: 占比({d}%)',
              formatter: '占比：{d}%',
            },
            color: ['#ee6666', '#fac858', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'],
          },
        ],
      },
    };
  },
  created() {
    console.log('this.dataList.length：', this.dataList.length);
    // 更新页面数据并渲染echarts图表
    this.updatePageAllData();
  },
  methods: {
    createEcharts() {
      if (!this.dataList.length) { return; }
      const chartDom = this.$refs.durationStatisticsChart;
      const charts = echarts.init(chartDom);

      this.dayList.unshift('product');
      this.dataList.unshift('duration');

      this.option.legend.data = this.dayList.slice(1, 8);
      this.option.dataset.source[0] = this.dayList;
      this.option.dataset.source[1] = this.dataList;

      // eslint-disable-next-line no-unused-expressions
      this.option && charts.setOption(this.option);
    },
    updatePageAllData() {
      this.spinning = true;
      getWeekUseDuration({ params: 'week_use_duration_statistics' })
        .then((res) => {
          const { data } = res.data;
          console.log(data);
          this.dataList = Object.values(data);
          console.log(this.dataList);
          this.dayList = Object.keys(data);
          this.$nextTick(() => this.createEcharts());
          this.spinning = false;
        })
        .catch((err) => {
          console.log(err.statusText);
          this.spinning = false;
        });
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
</style>
