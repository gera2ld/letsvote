import Vue from 'vue';
import VueRouter from 'vue-router';
import Poll from 'components/Poll';
import MyPolls from 'components/MyPolls';
import PollCreate from 'components/PollCreate';
import Callback from 'components/Callback';
import Portal from 'components/Portal';
import {store, user} from 'src/services';

Vue.use(VueRouter);

const requireLogin = (to, from, next) => {
  user.ready().then(() => {
    next(store.user.uid ? null : '/portal');
  });
};

const routes = [
  {
    path: '/',
    redirect: '/my/polls',
  },
  {
    path: '/portal',
    component: Portal,
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
