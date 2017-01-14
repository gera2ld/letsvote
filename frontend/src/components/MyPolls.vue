<template>
  <div class="flex-auto">
    <div class="card mb-10" v-for="question in questions">
      <div class="card-header">
        <span class="float-right" v-text="`${question.user_number} votes`"></span>
        <router-link :to="`/polls/${question.id}`">
          <h4 class="card-title" v-text="question.title"></h4>
        </router-link>
        <p class="card-meta" v-text="question.desc"></p>
      </div>
    </div>
  </div>
</template>

<script>
import { My } from 'src/services/restful';

export default {
  data() {
    return {
      questions: [],
    };
  },
  created() {
    My.Polls.get()
    .then(res => {
      this.questions = res.data;
    });
  },
};
</script>
