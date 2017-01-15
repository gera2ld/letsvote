<template>
  <div id="app" class="container grid-960 flex flex-col">
    <header class="navbar">
      <section class="navbar-section">
        <router-link to="/" class="navbar-brand mr-10">
          <img src="../static/vote.svg">
          <span class="hide-xs">Let's vote</span>
        </router-link>
        <router-link to="/my/polls" class="btn btn-link" active-class="active">My Polls</router-link>
        <router-link to="/polls/create" class="btn btn-link" active-class="active">Create Poll</router-link>
      </section>
      <section class="navbar-section">
        <figure class="avatar" v-if="store.user.uid">
          <img :src="store.user.avatar">
        </figure>
        <span class="hide-xs ml-5" v-text="store.user.nickname" v-if="store.user.uid"></span>
        <log-in v-if="!store.user.uid"></log-in>
      </section>
    </header>
    <router-view></router-view>
  </div>
</template>

<script>
import {store} from 'src/services';
import LogIn from 'components/LogIn';

export default {
  name: 'app',
  components: {
    LogIn,
  },
  data() {
    return {
      store,
    };
  },
};
</script>

<style>
html,
body,
#app {
  height: 100%;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.navbar-brand {
  font-size: 2rem;
  font-weight: bold;
  text-decoration: none;
  vertical-align: middle;
  color: inherit;
}

.navbar-brand > * {
  vertical-align: middle;
}

.navbar-brand > img {
  height: 2rem;
}

.flex-col {
  flex-direction: column;
}

.flex-auto {
  flex: auto;
  overflow: auto;
}

.flex-col > .flex-auto {
  height: 1px;
}
</style>
