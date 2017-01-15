<template>
  <div class="flex-auto empty mb-10">
    <p class="empty-title">Hey, dude!</p>
    <p class="empty-meta">Please log in and enjoy yourself!</p>
  </div>
</template>

<script>
import {store} from 'src/services';
import LogIn from './LogIn';

export default {
  components: {
    LogIn,
  },
  create() {
    if (store.user.uid) this.$router.push('/');
  },
};
</script>
