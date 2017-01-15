<template>
  <div class="card flex-auto mb-10 flex flex-col">
    <div class="card-header">
      <span class="card-meta float-right" v-text="`${question.user_number} votes`"></span>
      <h4 class="card-title" v-text="question.title"></h4>
      <p class="card-meta" v-text="question.desc"></p>
    </div>
    <div class="card-body flex-auto" v-if="question.selected || !store.user.uid">
      <div class="form-group" v-for="choice in question.choices">
        <div class="form-radio">
          <input type="radio" :value="choice.id" :checked="choice.checked">
          <i class="form-icon"></i> {{choice.title}}
        </div>
        <p v-text="choice.desc"></p>
        <div class="card-meta text-right" v-if="question.selected" v-text="`${choice.votes} votes`"></div>
      </div>
    </div>
    <form class="card-body flex-auto flex flex-col" @submit.prevent="onSubmit" v-else>
      <div class="flex-auto">
        <div class="form-group" v-for="choice in question.choices">
          <label class="form-radio">
            <input type="radio" :value="choice.id" v-model="picked">
            <i class="form-icon"></i> {{choice.title}}
          </label>
          <p v-text="choice.desc"></p>
        </div>
      </div>
      <div>
        <button class="btn btn-primary" :disabled="loading">Submit</button>
      </div>
    </form>
  </div>
</template>

<script>
import { Polls } from 'src/services/restful';
import { store } from 'src/services';

export default {
  data() {
    return {
      store,
      question: {
        title: 'Loading...',
        user_number: '?',
      },
      picked: null,
      loading: true,
    };
  },
  watch: {
    question(question) {
      question.selected && question.choices && question.choices.forEach(choice => {
        choice.checked = question.selected.includes(choice.id);
      });
    },
  },
  created() {
    const {id} = this.$route.params;
    Polls.get(id)
    .then(res => {
      this.question = res.data;
      this.loading = false;
    });
  },
  methods: {
    onSubmit() {
      const {id} = this.$route.params;
      const poll_values = [this.picked];
      this.loading = true;
      Polls.model(id).post(null, {poll_values})
      .then(res => {
        this.question = res.data;
        this.loading = false;
      });
    },
  },
};
</script>
