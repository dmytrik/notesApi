<template>
  <div class="auth">
    <h2>{{ isLogin ? "Login" : "Register" }}</h2>
    <form @submit.prevent="submit">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">{{ isLogin ? "Login" : "Register" }}</button>
    </form>
    <p @click="isLogin = !isLogin">
      {{ isLogin ? "Need to register?" : "Already have an account?" }}
    </p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useToast } from "vue-toastification";

export default defineComponent({
  name: "AuthView",
  setup() {
    const authStore = useAuthStore();
    const toast = useToast();
    return { authStore, toast };
  },
  data: () => ({
    email: "",
    password: "",
    isLogin: true,
  }),
  methods: {
    async submit() {
      try {
        const action = this.isLogin ? this.authStore.login : this.authStore.register;
        await action({ email: this.email, password: this.password });
        this.toast.success(`${this.isLogin ? "Login" : "Register"} successful!`);
        this.$router.push("/");
      } catch (e: any) {
        this.toast.error(e.response?.data?.detail || "Something went wrong");
      }
    },
  },
});
</script>

<style lang="scss" scoped>
@import "@/assets/scss/mixins";

.auth {
  max-width: $auth-width;
  margin: 0 auto;
  text-align: center;

  h2 {
    margin-bottom: $spacing-md;
  }

  form {
    @include flex-column;
    gap: $spacing-sm;

    input {
      padding: $spacing-sm;
      border: 1px solid $gray;
      border-radius: $border-radius;
    }

    button {
      @include button;
    }
  }

  p {
    margin-top: $spacing-sm;
    color: $primary;
    cursor: pointer;

    &:hover {
      text-decoration: underline;
    }
  }
}
</style>
