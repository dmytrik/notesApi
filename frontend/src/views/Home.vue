<template>
  <div class="home">
    <h2>Notes</h2>
    <form @submit.prevent="createNote">
      <textarea v-model="newNote" placeholder="Write a note..." required></textarea>
      <button type="submit">Add Note</button>
    </form>
    <NoteList :notes="notes" />
    <div class="actions">
      <button @click="$router.push('/analytics')">View Analytics</button>
      <button @click="logout">Logout</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useToast } from "vue-toastification";
import NoteList from "@/components/NoteList.vue";

export default defineComponent({
  name: 'HomeView',
  components: { NoteList },
  setup() {
    const authStore = useAuthStore();
    const toast = useToast();
    const notes = ref<any[]>([]);
    const newNote = ref('');

    onMounted(async () => {
      notes.value = await authStore.fetchNotes();
    });

    const createNote = async () => {
      try {
        const note = await authStore.createNote(newNote.value);
        notes.value.push(note);
        newNote.value = "";
        toast.success("Note created!");
      } catch (e: any) {
        toast.error(e.response?.data?.detail || "Failed to create note");
      }
    };

    const logout = () => {
      authStore.logout();
      window.location.href = "/auth";
    };

    return { notes, newNote, createNote, logout };
  },
});
</script>

<style lang="scss" scoped>
@import "@/assets/scss/variables";
@import "@/assets/scss/mixins";

.home {
  h2 {
    margin-bottom: $spacing-md;
  }

  form {
    @include flex-column;
    gap: $spacing-sm;
    margin-bottom: $spacing-lg;

    textarea {
      padding: $spacing-sm;
      border: 1px solid $gray;
      border-radius: $border-radius;
      min-height: 100px;
      resize: vertical;
    }

    button {
      @include button;
    }
  }

  .actions {
    @include flex-row;
    gap: $spacing-md;

    button {
      @include button;
    }
  }
}
</style>