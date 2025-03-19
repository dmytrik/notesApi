<template>
  <div class="note-analytics">
    <template v-if="analytics">
      <p>Total Word Count: {{ analytics.total_word_count }}</p>
      <p>Average Note Length: {{ analytics.average_note_length }}</p>
      <p>
        Most Common Words:
        {{ analytics.most_common_words.map((w: [string, number]) => `${w[0]} (${w[1]})`).join(", ") }}
      </p>
      <h3>Top 3 Longest Notes</h3>
      <ul>
        <li v-for="note in analytics.top_3_longest_notes" :key="note.id">
          {{ note.text }} ({{ note.word_count }} words)
        </li>
      </ul>
      <h3>Top 3 Shortest Notes</h3>
      <ul>
        <li v-for="note in analytics.top_3_shortest_notes" :key="note.id">
          {{ note.text }} ({{ note.word_count }} words)
        </li>
      </ul>
    </template>
    <p v-else>Loading analytics...</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";

export default defineComponent({
  name: 'NoteAnalytics',
  props: {
    analytics: {
      type: Object as PropType<any>,
      default: null,
    },
  },
});
</script>

<style lang="scss" scoped>
@import "@/assets/scss/variables";

.note-analytics {
  padding: $spacing-md;

  p {
    margin-bottom: $spacing-sm;
  }

  h3 {
    margin-top: $spacing-lg;
    margin-bottom: $spacing-sm;
  }

  ul {
    list-style: none;
    padding: 0;

    li {
      border: 1px solid $gray;
      padding: $spacing-sm;
      margin-bottom: $spacing-sm;
      border-radius: $border-radius;
    }
  }
}
</style>