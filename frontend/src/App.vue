<template>
  <div id="app">
    <router-view v-slot="{ Component, route }">
      <transition :name="route.meta.transition || 'fade'" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script setup lang="ts">
</script>

<style>
:root {
  --primary-color: #667eea;
  --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --secondary-color: #764ba2;
  --success-color: #52c41a;
  --warning-color: #faad14;
  --error-color: #f5222d;
  --text-color: #333333;
  --text-secondary: #666666;
  --text-tertiary: #999999;
  --border-color: #e8e8e8;
  --bg-color: #f5f5f5;
  --card-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  --card-radius: 16px;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: var(--primary-gradient);
  color: var(--text-color);
  line-height: 1.5;
}

#app {
  max-width: 600px;
  margin: 0 auto;
  min-height: 100vh;
  background: #ffffff;
  box-shadow: 0 0 40px rgba(0, 0, 0, 0.15);
  position: relative;
  overflow: hidden;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.van-hairline--bottom::after {
  border-bottom-color: var(--border-color);
}

::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

::-webkit-scrollbar-thumb {
  background: var(--primary-color);
  border-radius: 2px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::selection {
  background: var(--primary-color);
  color: #ffffff;
}
</style>