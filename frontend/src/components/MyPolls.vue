<template>
  <div class="flex-auto">
    <div class="card" v-for="poll in polls">
      <div class="card-header">
        <h4 class="card-title" v-text="poll.title"></h4>
        <p class="card-meta" v-text="poll.desc"></p>
      </div>
    </div>
  </div>
</template>

<script>
import { My } from 'src/services/restful';

function loadData() {
  return My.Polls.get()
  .then((res) => {
    console.log(res);
  });
}

export default {
  data() {
    return {
      polls: [],
    };
  },
  created() {
    loadData();
  },
  prefetch: loadData,
};
</script>
