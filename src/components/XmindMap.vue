<script setup lang="ts">
import { computed, ref } from 'vue'
import type { XmindNode } from '../utils/renderMarkdown'
import XmindBranch from './XmindBranch.vue'

const props = defineProps<{
  root: XmindNode
}>()

const BRANCH_COLORS = ['#1f9ed8', '#19c5b7', '#f2c200', '#ff8a00', '#ff4d4f', '#27c16f']
const MIN_SCALE = 0.5
const MAX_SCALE = 2
const SCALE_STEP = 0.1

const scale = ref(1)
const offsetX = ref(0)
const offsetY = ref(0)
const dragging = ref(false)
const collapsedIds = ref<string[]>([])

const dragStart = {
  x: 0,
  y: 0,
  offsetX: 0,
  offsetY: 0,
}

const topBranches = computed(() =>
  props.root.children.map((node, index) => ({
    node,
    color: BRANCH_COLORS[index % BRANCH_COLORS.length],
  })),
)

const zoomLabel = computed(() => `${Math.round(scale.value * 100)}%`)

function clampScale(next: number) {
  return Math.min(MAX_SCALE, Math.max(MIN_SCALE, Number(next.toFixed(2))))
}

function zoomIn() {
  scale.value = clampScale(scale.value + SCALE_STEP)
}

function zoomOut() {
  scale.value = clampScale(scale.value - SCALE_STEP)
}

function resetView() {
  scale.value = 1
  offsetX.value = 0
  offsetY.value = 0
}

function toggleNode(id: string) {
  if (collapsedIds.value.includes(id)) {
    collapsedIds.value = collapsedIds.value.filter((item) => item !== id)
    return
  }

  collapsedIds.value = [...collapsedIds.value, id]
}

function handlePointerDown(event: PointerEvent) {
  const target = event.target as HTMLElement | null
  if (target?.closest('button')) {
    return
  }

  dragging.value = true
  dragStart.x = event.clientX
  dragStart.y = event.clientY
  dragStart.offsetX = offsetX.value
  dragStart.offsetY = offsetY.value

  const currentTarget = event.currentTarget as HTMLElement | null
  currentTarget?.setPointerCapture?.(event.pointerId)
}

function handlePointerMove(event: PointerEvent) {
  if (!dragging.value) {
    return
  }

  offsetX.value = dragStart.offsetX + event.clientX - dragStart.x
  offsetY.value = dragStart.offsetY + event.clientY - dragStart.y
}

function handlePointerUp(event: PointerEvent) {
  dragging.value = false
  const currentTarget = event.currentTarget as HTMLElement | null
  currentTarget?.releasePointerCapture?.(event.pointerId)
}

function handleWheel(event: WheelEvent) {
  event.preventDefault()

  const delta = event.deltaY > 0 ? -SCALE_STEP : SCALE_STEP
  scale.value = clampScale(scale.value + delta)
}
</script>

<template>
  <div class="xmind-viewer">
    <div class="xmind-toolbar">
      <div class="toolbar-copy">
        <strong>思维导图视图</strong>
        <span>支持鼠标拖动、滚轮缩放、节点收起展开</span>
      </div>

      <div class="toolbar-actions">
        <button type="button" class="toolbar-btn" @click="zoomOut">缩小</button>
        <span class="zoom-label">{{ zoomLabel }}</span>
        <button type="button" class="toolbar-btn" @click="zoomIn">放大</button>
        <button type="button" class="toolbar-btn" @click="resetView">重置视图</button>
      </div>
    </div>

    <div
      class="xmind-viewport"
      :class="{ dragging }"
      @pointerdown="handlePointerDown"
      @pointermove="handlePointerMove"
      @pointerup="handlePointerUp"
      @pointerleave="handlePointerUp"
      @wheel="handleWheel"
    >
      <div
        class="xmind-stage"
        :style="{ transform: `translate(${offsetX}px, ${offsetY}px) scale(${scale})` }"
      >
        <div class="xmind-layout">
          <section class="mind-root">
            <div class="root-card">
              {{ root.title }}
            </div>
          </section>

          <section class="mind-branches">
            <ul class="branch-list">
              <XmindBranch
                v-for="branch in topBranches"
                :key="branch.node.id"
                :node="branch.node"
                :color="branch.color"
                :collapsed-ids="collapsedIds"
                :on-toggle="toggleNode"
              />
            </ul>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.xmind-viewer {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.xmind-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.04);
}

.toolbar-copy {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.toolbar-copy strong {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.92);
}

.toolbar-copy span {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.58);
}

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.toolbar-btn {
  padding: 8px 14px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.88);
  cursor: pointer;
}

.zoom-label {
  min-width: 56px;
  text-align: center;
  color: rgba(255, 255, 255, 0.72);
}

.xmind-viewport {
  overflow: hidden;
  min-height: 780px;
  padding: 24px;
  border-radius: 16px;
  background: #ffffff;
  cursor: grab;
  user-select: none;
}

.xmind-viewport.dragging {
  cursor: grabbing;
}

.xmind-stage {
  width: max-content;
  min-width: 1400px;
  transform-origin: top left;
  transition: transform 0.12s ease-out;
}

.xmind-layout {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 56px;
  align-items: center;
  min-height: 720px;
}

.mind-root {
  display: flex;
  justify-content: center;
}

.root-card {
  position: relative;
  padding: 16px 28px;
  border: 3px solid #6aa4f0;
  border-radius: 12px;
  background: #f7fbff;
  color: #1d4b88;
  font-size: 1.8rem;
  font-weight: 700;
  white-space: nowrap;
}

.root-card::after {
  content: '';
  position: absolute;
  right: -56px;
  top: 50%;
  width: 56px;
  height: 3px;
  background: #6aa4f0;
  transform: translateY(-50%);
}

.branch-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin: 0;
  padding: 0;
  list-style: none;
}

@media (max-width: 900px) {
  .xmind-toolbar {
    flex-direction: column;
    align-items: flex-start;
  }

  .xmind-viewport {
    min-height: 620px;
  }
}
</style>
