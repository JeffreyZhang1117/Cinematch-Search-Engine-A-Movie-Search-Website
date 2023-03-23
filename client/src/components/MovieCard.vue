<template>
  <div class="card">
    <div class="row">
      <div class="col-md-2">
        <img :src="movie.Poster" class="img-fluid rounded-start" :alt="movie.Title" />
      </div>
      <div class="col-md-10">
        <div class="card-body">
          <h5 class="card-title card-text" style="color: black">
            <a class="card-text" :href="`https://www.imdb.com/title/${movie.imdbID}`" target="_blank">{{ movie.Title }}</a>
            <span>({{ movie.Year }})</span>
            <span class="icon-down" :class="[isShow ? 'right_active' : 'bottom_active']" @click="toOpenDownList(movie._id)"></span>
          </h5>
          <p class="card-text">
            {{ movie.Runtime ? movie.Runtime : 'N/A' }}
            <span v-for="genre in movie.Genre.split(',')"> | {{ genre }}</span>
          </p>
          <p class="card-text" style="color: black">Director: {{ movie.Director ? movie.Director : 'N/A' }}</p>

          <p class="card-text" style="color: black">
            Actors: {{ movie.Actors ? movie.Actors : 'N/A' }}
            <span v-for="actor in movie.Actors.split(',')"> | {{ actor }}</span>
          </p>
          <p class="card-text">
            {{ movie.Plot == 'N/A' ? 'No Plot' : movie.Plot.replace(/(\r\n|\n|\r|\<>)/gm, '') }}
          </p>
        </div>
      </div>
    </div>
    <div v-if="isShow" class="show_wrap">
      <div class="card_title">Similar films you might like:</div>
      <div class="row show_row">
        <template v-for="(item, index) in relationList" :key="item._id">
          <div class="col-12-5">
            <div :class="{ is_loading: loading[index] }" v-if="loading[index]">Loading...</div>
            <img :src="item.Poster" class="img-fluid rounded-start col-img" :alt="item.Title" />
            <h5 class="card-title card-text" style="margin-top: 15px">
              <a class="card-text" :href="`https://www.imdb.com/title/${item.imdbID}`" target="_blank">{{ item.Title }}</a>
            </h5>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MovieCard',
  props: {
    href: String,
    movie: Object,
  },
  data() {
    return {
      isShow: false,
      api1: 'api/movies/relation',
      api2: '/api/movies/_id',
      relationList: [
        { Title: '', Genre: '', Actors: '' },
        { Title: '', Genre: '', Actors: '' },
        { Title: '', Genre: '', Actors: '' },
        { Title: '', Genre: '', Actors: '' },
        { Title: '', Genre: '', Actors: '' },
      ],
      loading: [false, false, false, false, false],
    }
  },
  methods: {
    async toOpenDownList(id) {
      this.isShow = !this.isShow
      if (!this.isShow) return
      for (let i = 0; i < this.loading.length; i++) {
        this.loading[i] = true
      }
      fetch(`${this.api1}?id=${id}`)
        .then((res) => res.json())
        .then((data) => {
          if (data.response === 'success') {
            const ids = data.movies.map((item) => item[0])
            this.getRelationList(ids)
          }
        })
    },
    getRelationList(list) {
      list.forEach(async (ele, index) => {
        fetch(`${this.api2}/${ele}`)
          .then((res) => res.json())
          .then((data) => {
            if (data.response === 'success') {
              this.relationList[index] = data.movie
            }
            this.loading[index] = false
          })
      })
    },
  },
  watch: {
    $route() {
      this.isShow = false
    },
  },
}
</script>

<style scoped>
img {
  padding: 2ch;
  width: 100%;
  height: 8vm;
  object-fit: cover;
}
.card {
  background-color: rgba(128, 209, 200, 0.45);
}
.show_wrap {
  box-sizing: border-box;
  width: 100%;
  background-color: rgba(28, 180, 163, 0.6);
}
.show_wrap > .show_row:last-child {
  border-width: 0px;
}
.show_row {
  margin-left: 0 !important;
  margin-right: 0 !important;
  padding: 0 2%;
  display: flex;
  border-bottom: 2px solid rgb(128, 209, 200);
}
.col-img {
  padding: 0;
}
.col-12-5 {
  box-shadow: 0 0 10px rgb(96, 96, 96);
  border-radius: 10px;
  margin: 10px 10px;
  position: relative;
  flex: 1;
  display: flex;
  padding: 15px 40px 15px 40px;
  flex-wrap: wrap;
}

.card-text {
  text-align: left;
  text-decoration: none !important;
}
p {
  width: 100%;
}
.card-img-top {
  width: 80%;
  height: 20vw;
  object-fit: cover;
}
.icon-down {
  cursor: pointer;
  float: right;
  border-top: 10px solid transparent;
  border-bottom: 10px solid transparent;
  border-right: 10px solid transparent;
  border-left: 10px solid #333;
}

.icon-down:hover {
  cursor: pointer;
  float: right;
  border-top: 10px solid transparent;
  border-bottom: 10px solid transparent;
  border-right: 10px solid transparent;
  border-left: 10px solid #ffd700;
}

.right_active {
  transform: rotate(90deg);
  transition: all 0.5s;
}
.bottom_active {
  transform: rotate(0deg);
  transition: all 0.5s;
}
.is_loading {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 30px;
  background-color: rgba(167, 170, 173);
  z-index: 1000;
  position: absolute;
  height: 100%;
  width: 100%;
  border-radius: 10px;
  left: 0;
  top: 0;
  color: #666;
  text-align: center;
}
.card_title {
  height: 40px;
  line-height: 40px;
  font-size: 24px;
  margin-left: 2%;
  font-weight: bold;
  padding-left: 6px;
  margin-top: 12px;
  border-left: 5px solid #ffd4a9;
}
</style>
