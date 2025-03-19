<template>
  <div class="note-list">
    <div v-for="note in notes" :key="note.id" class="note">
      <p>{{ note.text }}</p>
      <p class="summary">{{ note.summary }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";

export default defineComponent({
  name: "NoteList",
  props: {
    notes: {
      type: Array as PropType<any[]>,
      required: true,
    },
  },
});
</script>

<style lang="scss" scoped>
@import "@/assets/scss/variables";

.note-list {
  margin-top: $spacing-lg;

  .note {
    border: 1px solid $gray;
    padding: $spacing-md;
    margin-bottom: $spacing-sm;
    border-radius: $border-radius;

    .summary {
      font-style: italic;
      color: $dark-gray;
    }
  }
}
</style>