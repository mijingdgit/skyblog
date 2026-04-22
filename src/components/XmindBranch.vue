<script setup lang="ts">
defineOptions({ name: 'XmindBranch' })

import { computed } from 'vue'
import type { XmindNode } from '../utils/renderMarkdown'

const props = withDefaults(
  defineProps<{
    node: XmindNode
    color: string
    collapsedIds: string[]
    onToggle: (id: string) => void
    level?: number
  }>(),
  {
    level: 1,
  },
)

const isCollapsed = computed(() => props.collapsedIds.includes(props.node.id))
const hasChildren = computed(() => props.node.children.length > 0)
</script>

<template>
  <li class="branch-node" :class="`level-${level}`" :style="{ '--branch-color': color }">
    <div class="branch-row">
      <div class="branch-card">
        <span class="branch-title">{{ node.title }}</span>
      </div>

      <button
        v-if="hasChildren"
        type="button"
        class="branch-toggle"
        :aria-label="isCollapsed ? '展开节点' : '收起节点'"
        @click.stop="onToggle(node.id)"
      >
        {{ isCollapsed ? '+' : '-' }}
      </button>
    </div>

    <ul v-if="hasChildren && !isCollapsed" class="branch-children">
      <XmindBranch
        v-for="child in node.children"
        :key="child.id"
        :node="child"
        :color="color"
        :collapsed-ids="collapsedIds"
        :on-toggle="onToggle"
        :level="level + 1"
      />
    </ul>
  </li>
</template>

<style scoped>
.branch-node {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.branch-row {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.branch-row::before {
  content: '';
  position: absolute;
  left: -36px;
  top: 50%;
  width: 36px;
  height: 2px;
  background: var(--branch-color);
  transform: translateY(-50%);
}

.branch-card {
  min-width: 150px;
  max-width: 420px;
  padding: 8px 14px;
  border: 2px solid #6aa4f0;
  border-radius: 8px;
  background: #fff;
  color: #1d3f74;
  font-size: 0.95rem;
  line-height: 1.5;
  word-break: break-word;
}

.branch-title {
  display: block;
}

.branch-toggle {
  width: 20px;
  height: 20px;
  padding: 0;
  border: 1px solid var(--branch-color);
  border-radius: 50%;
  background: #fff;
  color: var(--branch-color);
  font-size: 0.85rem;
  line-height: 1;
  cursor: pointer;
}

.branch-children {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 0 0 0 34px;
  padding: 4px 0 0 36px;
  list-style: none;
}

.branch-children::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 18px;
  width: 2px;
  background: var(--branch-color);
}

.level-1 > .branch-row > .branch-card {
  min-width: 170px;
  font-size: 1rem;
}
</style>
