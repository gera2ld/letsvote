import Vue from 'vue';
import VueRouter from 'vue-router';
import Main from 'components/Main';
import Poll from 'components/Poll';
import PollList from 'components/PollList';
import PollCreate from 'components/PollCreate';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    component: Main,
  },
  {
    path: '/my/polls',
    component: PollList,
  },
  {
    path: '/polls/create',
    component: PollCreate,
  },
  {
    path: '/polls/:id',
    component: Poll,
  },
];

const router = new VueRouter({
  routes,
  mode: 'history',
});

export default router;
