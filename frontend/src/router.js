import Vue from 'vue';
import VueRouter from 'vue-router';
import Poll from 'components/Poll';
import MyPolls from 'components/MyPolls';
import PollCreate from 'components/PollCreate';
import Callback from 'components/Callback';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    redirect: '/my/polls',
  },
  {
    path: '/my/polls',
    component: MyPolls,
  },
  {
    path: '/polls/create',
    component: PollCreate,
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
