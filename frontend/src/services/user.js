import store from './store';
import {loadCache, dumpCache} from './cache';
import restful from './restful';
const USER_KEY = '__user';
load();

function loadToken() {
  const token = store.user && store.user.token;
  restful.options.headers['Authorization'] = token ? `token ${token}` : null;
}

export function load() {
  store.user = loadCache(USER_KEY);
  loadToken();
}

export function dump(user) {
  if (user) {
    user.token = user.token || store.user && store.user.token;
  }
  store.user = user;
  dumpCache(USER_KEY, user);
  loadToken();
}
