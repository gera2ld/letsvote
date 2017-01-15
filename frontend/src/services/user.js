import store from './store';
import {loadCache, dumpCache} from './cache';
import restful from './restful';
const USER_KEY = '__user';
load();

var retrieving;

function loadToken() {
  const token = store.user && store.user.token;
  restful.options.headers['Authorization'] = token ? `token ${token}` : null;
}

export function ready() {
  return retrieving;
}

export function retrieve() {
  return retrieving = restful.get('me')
  .then(user => {
    store.user = Object.assign({}, store.user, user);
  }, err => {
    if (err.status === 401) {
      dump({arbiter: err.data.log_in});
    }
  });
}

function load() {
  store.user = loadCache(USER_KEY) || {};
  loadToken();
  retrieve();
}

export function dump(user) {
  if (user && user.uid) {
    user.token = user.token || store.user && store.user.token;
  }
  store.user = user;
  dumpCache(USER_KEY, user && ['uid', 'token'].reduce((res, key) => {
    res[key] = user[key];
    return res;
  }, {}));
  loadToken();
}
