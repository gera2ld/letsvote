<template>
  <button class="btn btn-primary" @click.prevent="onClick" v-if="user.arbiter">Log In</button>
</template>

<script>
import {store} from 'src/services';

export default {
  data() {
    return store;
  },
  methods: {
    onClick() {
      const {arbiter} = this.user;
      const url = `${location.protocol}//${location.host}/callback?next=${encodeURIComponent(location.pathname)}`;
      location.href = `${arbiter}?next=${encodeURIComponent(url)}`;
    },
  },
};
</script>
