<template>
  <div class="analytics">
    <h2>Notes Analytics</h2>
    <NoteAnalytics :analytics="analytics" />
    <button @click="$router.push('/')">Back to Notes</button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import NoteAnalytics from "@/components/NoteAnalytics.vue";

export default defineComponent({
  name: "AnalyticsView",
  components: { NoteAnalytics },
  setup() {
    const authStore = useAuthStore();
    const analytics = ref<any>(null);

    onMounted(async () => {
      analytics.value = await authStore.fetchAnalytics();
    });

    return { analytics };
  },
});
</script>

<style lang="scss" scoped>
@import "@/assets/scss/variables";
@import "@/assets/scss/mixins";

.analytics {
  h2 {
    margin-bottom: $spacing-md;
  }

  button {
    @include button;
    margin-top: $spacing-lg;
  }
}
</style>