import store from './store';
import {loadCache, dumpCache} from './cache';
import restful from './restful';
const USER_KEY = '__user';
load();

function loadToken() {
  const token = store.user && store.user.token;
  restful.options.headers['Authorization'] = token ? `token ${token}` : null;
}

export function retrieve() {
  return restful.get('me')
  .then(user => {
    store.user = Object.assign({}, store.user, user);
  }, err => {
    if (err.status === 401) {
      dump();
      const {log_in} = err.data;
      log_in && setTimeout(() => {
        const url = `${location.protocol}//${location.host}/callback?next=${encodeURIComponent(location.pathname)}`;
        location.href = `${log_in}?next=${encodeURIComponent(url)}`;
      }, 3000);
    }
  });
}

export function load() {
  store.user = loadCache(USER_KEY);
  loadToken();
  store.user && store.user.token && retrieve();
}

export function dump(user) {
  if (user) {
    user.token = user.token || store.user && store.user.token;
  }
  store.user = user;
  dumpCache(USER_KEY, user && ['id', 'token'].reduce((res, key) => {
    res[key] = user[key];
    return res;
  }, {}));
  loadToken();
}
