export const compareObjectsValues = (valueX, valueY) => {
  const valueXStr = JSON.stringify(valueX);
  const valueYStr = JSON.stringify(valueY);
  return valueXStr === valueYStr;
};

export const timeRangeValidator = (timeValue) => {
  const date = new Date();
  const year = date.getFullYear();
  // const timeBit = ['年', '月', '日', '时', '分', '秒', '星期'];

  const timeValueArray = timeValue
    .substring(1, timeValue.length - 1).split(',');

  const validator = { flag: true };
  const rangeRules = [{ max: 9999, min: year }, { max: 12, min: 1 },
    { max: 31, min: 1 }, { max: 23, min: 0 }, { max: 59, min: 0 },
    { max: 59, min: 0 }, { max: 7, min: 1 }];

  // 遍历时间规则数组，当不满足条件时立刻退出并返回验证不通过
  timeValueArray.some((items, index) => {
    const { max, min } = rangeRules[index];

    // 当该位的值中包含有符号“-”时进入
    if (/\-/.test(items)) {
      const [ts, te] = items.split('-');
      const tStart = Number(ts);
      const tStop = Number(te);
      // 当时间范围符合规则时验证通过，否则跳出循环验证不通过
      validator.flag = !((tStop > max || tStart < min)
        || (tStart >= tStop));
      return !validator.flag;
    }

    // 当该为的值为数值类型时进入
    if (/\d/.test(items)) {
      // 当不满足 min<=items<=max 时退出并验证不通过
      validator.flag = !(items > max || items < min);
      return !validator.flag;
    }
  });

  return validator.flag;
};
