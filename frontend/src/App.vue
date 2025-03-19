<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "App",
});
</script>

<style lang="scss" scoped>
@import "@/assets/scss/variables";

#app {
  font-family: $font-family;
  max-width: $max-width;
  margin: 0 auto;
  padding: $spacing-lg;
}
</style>