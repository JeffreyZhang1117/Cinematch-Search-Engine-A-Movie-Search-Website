<template>
  <div class="not_found">
    <div class="conotent-wrap">
      <div class="content1">
        <h1>Sorry, no result for it.</h1>
      </div>
      <div class="content2">
        <h1>We are working hard to enlarge our database.</h1>
        <h1>Please try another keywords in the searching box.</h1>
        <h1>Thanks for your patience.</h1>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ErrorPage',
}
</script>

<style scoped>
/* .background {
  width: 100%;
  height: 100%;
  z-index: -1;
  position: fixed;
  background: rgba(255, 255, 255, .);
} */
.not_found {
  left: 0;
  position: fixed;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  top: 0;
  bottom: 0;
  right: 0;
}
.conotent-wrap {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 1px solid rgba(46, 46, 46, 0.125);
  padding: 30px 10px;
  background-color: rgba(255, 255, 255, 0.75);
  border-radius: 10px;
}
.content1 {
  text-align: center; /*让div内部文字居中*/
  color: red;
  height: 70px;
  line-height: 70px;
  width: 500px;
}
.content2 {
  text-align: center; /*让div内部文字居中*/
  color: rgb(136, 136, 136);
  width: 1000px;
}
</style>
