const localstory = window.localStorage;

/**
 * localstroy 保存 key :vlaue
 * @param {*} key
 * @param {*} value
 */
export function localSetItem(key, value) {
  localstory.setItem(key, value);
}

/**
 * localstroy 读取 key
 * @param {*} key
 */
export function localgetItem(key) {
  return localstory.getItem(key);
}

/**
 * localstroy 删除 key
 * @param {*} key
 */
export function localRemoveItem(key) {
  localStorage.removeItem(key);
}

/**
 * 清除 localstroy
 */
export function localClear() {
  localStorage.clear();
}
