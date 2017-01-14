<template>
  <form class="flex flex-col flex-auto" @submit.prevent="onSubmit">
    <div class="form-group">
      <input class="form-input" v-model="question.title" required placeholder="Question">
    </div>
    <div class="form-group">
      <textarea class="form-input" v-model="question.desc" placeholder="Description"></textarea>
    </div>
    <div class="flex-auto">
      <div class="card mb-10" v-for="(choice, index) in choices" :key="choice">
        <div class="card-header">
          <button class="btn btn-clear float-right" type="button" @click="removeChoice(index)"></button>
          <h4 class="card-title">Choice #{{index + 1}}</h4>
        </div>
        <div class="card-body form-horizontal">
          <div class="form-group">
            <input class="form-input" v-model="choice.title" placeholder="Choice">
          </div>
          <div class="form-group">
            <textarea class="form-input" v-model="choice.desc" placeholder="Description"></textarea>
          </div>
        </div>
      </div>
    </div>
    <div class="form-group columns">
      <div class="column">
        <button class="btn" type="button" @click="addChoice">Add choice</button>
      </div>
      <div class="column text-right">
        <button class="btn btn-primary">Submit</button>
      </div>
    </div>
  </form>
</template>

<script>
import { Polls } from 'src/services/restful';

export default {
  data() {
    return {
      question: {},
      choices: [{}],
    };
  },
  methods: {
    addChoice() {
      this.choices.push({});
    },
    removeChoice(index) {
      this.choices.splice(index, 1);
    },
    onSubmit() {
      const question = {
        title: this.question.title,
        desc: this.question.desc,
      };
      const choices = this.choices.filter(choice => choice.title)
      .map(choice => ({title: choice.title, desc: choice.desc}));
      if (!question.title || !choices.length) return;
      const data = {
        question,
        choices,
      };
      Polls.post(null, data)
      .then(res => {
        this.$router.push(`/polls/${res.data.id}`);
      });
    },
  },
};
</script>
