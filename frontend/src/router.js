import Vue from 'vue';
import VueRouter from 'vue-router';
import Poll from 'components/Poll';
import MyPolls from 'components/MyPolls';
import PollCreate from 'components/PollCreate';
import Callback from 'components/Callback';
import {store, user} from 'src/services';

Vue.use(VueRouter);

const requireLogin = (to, from, next) => {
  (store.user && store.user.token ? Promise.resolve() : user.retrieve())
  .then(next);
};

const routes = [
  {
    path: '/',
    redirect: '/my/polls',
  },
  {
    path: '/my/polls',
    component: MyPolls,
    beforeEnter: requireLogin,
  },
  {
    path: '/polls/create',
    component: PollCreate,
    beforeEnter: requireLogin,
  },
  {
    path: '/polls/:id',
    component: Poll,
  },
  {
    path: '/callback',
    component: Callback,
  },
];

const router = new VueRouter({
  routes,
  mode: 'history',
});

export default router;
