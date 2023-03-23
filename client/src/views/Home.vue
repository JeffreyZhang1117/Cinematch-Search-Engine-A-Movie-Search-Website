<template>
  <div class="home">
    <div class="container header">
      <div class="logo">
        <router-link :to="'/'" custom v-slot="{ href }">
          <a :href="href"><img src="../../public/logos/logo.png" width="220" height="150" alt="" /></a>
        </router-link>
      </div>
      <search-bar class="search-bar" :sory="sort"></search-bar>
    </div>
    <div class="tip container">
      <h3 class="result" v-if="this.$route.path == '/search' || this.$route.path == '/searchAll'">
        Results for '{{ Object.values(this.$route.query)[0] }}'
      </h3>
      <div class="select" v-if="this.$route.path == '/search' || this.$route.path == '/searchAll'">
        <span class="sortby">sort by: </span>
        <button
          class="btn btn-info dropdown-toggle select-btn"
          type="button"
          id="dropdownMenuButton1"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          {{ sortBy }}
        </button>
        <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
          <li v-for="item in sort">
            <button class="dropdown-item" @click="toSearchMovie(item)">
              {{ item }}
            </button>
          </li>
        </ul>
      </div>
    </div>
    <div
      :class="{
        resultpage: this.$route.path == '/search' || this.$route.path == '/searchAll',
        infopage: this.$route.path != '/search' && this.$route.path != '/searchAll',
      }"
    >
      <div
        :class="{
          container: this.$route.path == '/search' || this.$route.path == '/searchAll',
        }"
      >
        <router-view v-slot="{ Component, route }">
          <keep-alive>
            <component :is="Component" :key="route.name" v-if="route.meta.keepAlive" />
          </keep-alive>
          <component :is="Component" :key="route.name" v-if="!route.meta.keepAlive" />
        </router-view>
      </div>
    </div>
  </div>
</template>

<script>
import SearchBar from '../components/SearchBar.vue'

export default {
  name: 'Home',
  components: {
    SearchBar,
  },
  data() {
    return {
      sort: ['relevance', 'popularity', 'rating', 'release_date'],
      sortBy: 'relevance',
    }
  },
  methods: {
    toSearchMovie(item) {
      this.sortBy = item
      const query = this.$route.query
      this.$router.push({
        path: '/search',
        query: { ...query, sort: this.sortBy },
      })
    },
  },
}
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.header {
  /* background-color: aqua; */
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-right: 0;
}
.resultpage {
  margin-top: 10px;
}
.logo {
  flex: 0.2;
}
.search-bar {
  flex: 0.8;
}
.tip {
  height: 70px;
  display: flex;
  justify-content: space-between !important;
  align-items: center;
}
.result {
  color: rgb(0, 0, 0);
}
.container {
  display: flex;
  z-index: 1200;
  justify-content: center;
  align-items: center;
}
.select {
  z-index: 1000;
}
.sortby {
  font-size: 20px;
  margin-right: 5px;
  font-weight: 800;
  color: #555;
  vertical-align: -2px;
}
</style>
