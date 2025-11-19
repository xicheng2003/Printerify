<template>
  <div class="theme-switcher-wrapper" ref="wrapperRef">
    <button
      @click="toggleMenu"
      class="theme-btn"
      :aria-label="currentLabel"
      :title="currentLabel"
    >
      <component :is="currentIcon" class="w-5 h-5" />
    </button>

    <Transition name="fade-scale">
      <div v-if="isOpen" class="theme-menu">
        <div class="menu-title">外观</div>
        <button
          v-for="option in options"
          :key="option.value"
          @click="selectTheme(option.value)"
          class="menu-item"
          :class="{ active: themeStore.theme === option.value }"
        >
          <component :is="option.icon" class="menu-icon" />
          <span class="menu-label">{{ option.label }}</span>
          <span v-if="themeStore.theme === option.value" class="check-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
          </span>
        </button>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, h } from 'vue';
import { useThemeStore } from '@/stores/theme';

const themeStore = useThemeStore();
const isOpen = ref(false);
const wrapperRef = ref(null);

// Icons
const IconSun = {
  render: () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', width: '20', height: '20', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
    h('circle', { cx: '12', cy: '12', r: '5' }),
    h('line', { x1: '12', y1: '1', x2: '12', y2: '3' }),
    h('line', { x1: '12', y1: '21', x2: '12', y2: '23' }),
    h('line', { x1: '4.22', y1: '4.22', x2: '5.64', y2: '5.64' }),
    h('line', { x1: '18.36', y1: '18.36', x2: '19.78', y2: '19.78' }),
    h('line', { x1: '1', y1: '12', x2: '3', y2: '12' }),
    h('line', { x1: '21', y1: '12', x2: '23', y2: '12' }),
    h('line', { x1: '4.22', y1: '19.78', x2: '5.64', y2: '18.36' }),
    h('line', { x1: '18.36', y1: '5.64', x2: '19.78', y2: '4.22' })
  ])
};

const IconMoon = {
  render: () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', width: '20', height: '20', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
    h('path', { d: 'M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z' })
  ])
};

const IconSystem = {
  render: () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', width: '20', height: '20', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
    h('rect', { x: '2', y: '3', width: '20', height: '14', rx: '2', ry: '2' }),
    h('line', { x1: '8', y1: '21', x2: '16', y2: '21' }),
    h('line', { x1: '12', y1: '17', x2: '12', y2: '21' })
  ])
};

const options = [
  { label: '浅色', value: 'light', icon: IconSun },
  { label: '深色', value: 'dark', icon: IconMoon },
  { label: '跟随系统', value: 'system', icon: IconSystem }
];

const currentIcon = computed(() => {
  const option = options.find(o => o.value === themeStore.theme);
  return option ? option.icon : IconSystem;
});

const currentLabel = computed(() => {
  const option = options.find(o => o.value === themeStore.theme);
  return option ? `当前主题：${option.label}` : '切换主题';
});

const toggleMenu = () => {
  isOpen.value = !isOpen.value;
};

const selectTheme = (value) => {
  themeStore.setTheme(value);
  isOpen.value = false;
};

const handleClickOutside = (event) => {
  if (wrapperRef.value && !wrapperRef.value.contains(event.target)) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
.theme-switcher-wrapper {
  position: relative;
  display: inline-block;
}

.theme-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  transition: background-color 0.2s, color 0.2s;
  color: var(--color-text-mute);
}

.theme-btn:hover {
  background-color: var(--color-background-mute);
  color: var(--color-heading);
}

.theme-menu {
  position: absolute;
  top: 120%;
  right: 0;
  width: 180px;
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  padding: 0.5rem;
  z-index: 100;
  transform-origin: top right;
}

.menu-title {
  padding: 0.5rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--color-text-mute);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.menu-item {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 0.625rem 0.75rem;
  border: none;
  background: none;
  color: var(--color-text);
  font-size: 0.875rem;
  cursor: pointer;
  border-radius: 8px;
  transition: background-color 0.2s;
  text-align: left;
}

.menu-item:hover {
  background-color: var(--color-background-mute);
}

.menu-item.active {
  color: var(--color-primary);
  font-weight: 500;
}

.menu-icon {
  margin-right: 0.75rem;
  width: 18px;
  height: 18px;
  opacity: 0.8;
}

.menu-item.active .menu-icon {
  opacity: 1;
}

.check-icon {
  margin-left: auto;
  color: var(--color-primary);
}

/* Animation */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
