<template>
  <div id="app" class="container grid-960 flex flex-col">
    <header class="navbar">
      <section class="navbar-section">
        <a href="/" class="navbar-brand mr-10">
          <img src="../static/vote.svg">
          <span class="hide-xs">Let's vote</span>
        </a>
        <router-link to="/my/polls" class="btn btn-link" active-class="active">My Polls</router-link>
        <router-link to="/polls/create" class="btn btn-link" active-class="active">Create Poll</router-link>
      </section>
    </header>
    <router-view class="flex-auto"></router-view>
  </div>
</template>

<script>
export default {
  name: 'app',
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
}
</style>
