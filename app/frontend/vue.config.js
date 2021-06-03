/* 前端服务运行配置 */
const frontendPort = 8001; // 前端服务端口

/* 后端服务器地址配置 */
const backendHost = '127.0.0.1'; // 后端ip地址
const backendPort = 8000; // 后端端口

// vue配置
module.exports = {
  devServer: {
    port: frontendPort,
    open: true,
    overlay: {
      warnings: false,
      errors: true,
    },
    // 配置请求代理
    proxy: {
      '/api': { // 这里最好有一个
        target: `http://${backendHost}:${backendPort}`, // 开发服务器
        ws: true,
        changeOrigin: true, // 是否跨域
        pathRewrite: {
          '^/api': '/api',
        },
      },
    },
  },
  css: {
    loaderOptions: {
      less: {
        lessOptions: {
          javascriptEnabled: true,
        },
      },
    },
  },

  assetsDir: 'static', // 设置打包后静态文件（js、css、img）相对dist的目录
};
