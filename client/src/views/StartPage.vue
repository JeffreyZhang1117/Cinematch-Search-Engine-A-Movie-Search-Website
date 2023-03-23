<template>
  <div class="start">
    <img src="../../public/logos/logo.png" class="logo" />
    <search-bar :sort="['relevance', 'popularity', 'rating', 'release_date']"></search-bar>
  </div>
  <!-- <dropdown></dropdown> -->
</template>

<script>
import SearchBar from '../components/SearchBar.vue'
import Dropdown from '../components/Dropdown.vue'

export default {
  name: 'Start Page',
  components: {
    SearchBar,
    Dropdown,
  },
}
</script>

<style scoped>
.start {
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  padding-bottom: 100px;
}

.logo {
  width: 300px;
  height: 225px;
}
</style>
