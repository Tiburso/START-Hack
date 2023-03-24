<template>
  <div class="hello">
    <MyHeader></MyHeader>
    <div class="parent-container">
    <GameComponent>
      <!-- Put your card content here -->
    </GameComponent>
  </div>
    <MyFooter></MyFooter>
  </div>

</template>

<script>
import MyFooter from '@/components/MyFooter.vue'
import MyHeader from '@/components/MyHeader.vue'
import GameComponent from '@/components/GameComponent.vue'
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  components: {
    MyFooter,
    MyHeader,
    GameComponent
  },

}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.parent-container {
  display: flex;
  justify-content: space-between;
}
.hello{
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
}
</style>
