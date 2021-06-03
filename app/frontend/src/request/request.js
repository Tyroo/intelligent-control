import axios from 'axios';
import { notification } from 'ant-design-vue';

import { localgetItem } from './localstory';

// create an axios instance
const service = axios.create({
  // baseURL: '/api', // develop url
  baseURL: '/api', // production url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 5000, // request timeout
});

// request interceptor
service.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('x-token');
    if (token) {
      config.headers['x-token'] = token;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
   */
  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  (response) => {
    const { data } = response;
    if (data.statusCode !== 200) {
      notification.error({
        message: data.statusText || 'Error',
        description:
          '服务器响应异常',
        duration: 2,
      });
      return Promise.reject(response);
    }
    return Promise.resolve(response);
  },
  (error) => {
    const { response } = error;
    const { data } = response;
    if (response.status === 302 || response.status === 401) {
      localStorage.removeItem('x-token');
      window.location = response.data.redirect;
    }
    notification.error({
      message: data.statusText || 'Unknown error!',
      description:
        '服务器响应异常',
      duration: 2,
    });
    return Promise.reject(response);
  },
);

export default service;

/**
 * 封装 get 请求
 * @param {*请求地址} url
 * @param {*请求参数} params
 */
export const get = (url, params = {}) => new Promise((resolve, reject) => {
  service.get(url, {
    params,
  })
    .then((response) => {
      // resolve(response.data);
      resolve(response);
    })
    .catch((err) => {
      reject(err);
    });
});

/**
 * 封装 post 请求
 * @param {*请求地址} url
 * @param {*请求参数} data
 */
export const post = (url, data = {}) => new Promise((resolve, reject) => {
  service.post(url, data).then((response) => {
    resolve(response);
  }).catch((err) => {
    reject(err);
  });
});

/**
 * 封装 put 请求
 * @param {*请求地址} url
 * @param {*请求参数} data
 */
export const put = (url, data = {}) => new Promise((resolve, reject) => {
  service.put(url, data)
    .then((response) => {
      resolve(response);
    }, (err) => {
      reject(err);
    });
});

/**
 * 封装delete方法
 * @param {*请求地址} url
 * @param {*请求参数} params
 */
export const del = (url, params = {}) => new Promise((resolve, reject) => {
  service.delete(url, {
    params,
  })
    .then((response) => {
      resolve(response);
    })
    .catch((err) => {
      reject(err);
    });
});

export const upload = (url, params) => {
  const config = {
    headers: { 'Content-Type': 'multipart/form-data' },
  };
  return new Promise((resolve, reject) => {
    service.post(url, params, config)
      .then((response) => {
        resolve(response);
      })
      .catch((err) => {
        reject(err);
      });
  });
};
