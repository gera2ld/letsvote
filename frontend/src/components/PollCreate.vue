<template>
  <form class="flex flex-col">
    <div class="form-group">
      <input class="form-input" v-model="question.title" required placeholder="Question">
    </div>
    <div class="form-group">
      <textarea class="form-input" v-model="question.desc" placeholder="Description"></textarea>
    </div>
    <div class="flex-auto choice-list">
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
  },
};
</script>

<style scoped>
.choice-list {
  height: 1px;
  overflow: auto;
}
</style>
