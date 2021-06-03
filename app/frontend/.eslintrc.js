module.exports = {
  env: {
    browser: true,
    es6: true,
  },
  extends: [
    'plugin:vue/essential',
    'airbnb-base',
  ],
  globals: {
    Atomics: 'readonly',
    SharedArrayBuffer: 'readonly',
  },
  parserOptions: {
    ecmaVersion: 2018,
    sourceType: 'module',
    parser: 'babel-eslint',
  },
  plugins: [
    'vue',
  ],
  rules: {
    'import/extensions': 0,
    'import/no-extraneous-dependencies': [2, { devDependencies: true }],
    'import/no-unresolved': 0,
    // 是否允许console打印
    'no-console': 1,
    // 每行最多的字符数
    'max-len': [1, { code: 300 }],
    'no-unused-vars': 0,
    'global-require': 0,
    'vue/no-v-model-argument': 0,
    'no-param-reassign': 0,
    'consistent-return': 0,
    'import/prefer-default-export': 0,
    'prefer-object-spread': 0,
    'no-useless-escape': 0,
    'array-callback-return': 0,
    'no-sequences': 0,
    'no-plusplus': 0,
    'prefer-const': 0,
  },
};
