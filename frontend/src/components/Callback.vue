<template>
  <div class="empty">
    <p class="empty-title" v-text="message"></p>
    <div class="loading" v-if="loading"></div>
  </div>
</template>

<script>
import {user, restful} from 'src/services';

export default {
  data() {
    return {
      loading: true,
      message: 'Authorizing...',
    };
  },
  created() {
    const {ticket, next} = this.$route.query;
    if (!ticket) {
      this.loading = false;
      this.message = 'Oops, authorization failed!';
      return;
    }
    restful.get('/authorize', {ticket})
    .then(data => {
      user.dump(data);
      this.$router.replace(next || '/');
    }, err => {
      console.error(err);
    });
  },
};
</script>
