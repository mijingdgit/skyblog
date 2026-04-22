<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, ref, shallowRef, watch } from 'vue'
import { XMindEmbedViewer } from 'xmind-embed-viewer'

const props = defineProps<{
  fileUrl: string
}>()

const viewportRef = ref<HTMLElement | null>(null)
const containerRef = ref<HTMLElement | null>(null)
const viewer = shallowRef<XMindEmbedViewer | null>(null)
const isLoading = ref(true)
const loadError = ref('')
const zoomScale = ref(100)
const isPanMode = ref(false)
const isPanning = ref(false)
const panStart = ref({
  x: 0,
  y: 0,
  left: 0,
  top: 0,
})
let loadSerial = 0

const normalizedUrl = computed(() => {
  if (!props.fileUrl) {
    return ''
  }

  if (/^https?:\/\//i.test(props.fileUrl)) {
    return props.fileUrl
  }

  return props.fileUrl.startsWith('/') ? props.fileUrl : `/${props.fileUrl}`
})

const hostStyle = computed(() => {
  const scale = Math.max(1, zoomScale.value / 100)

  return {
    width: `max(100%, ${Math.round(2200 * scale)}px)`,
    height: `${Math.round(1800 * scale)}px`,
  }
})

function centerViewport() {
  requestAnimationFrame(() => {
    const viewport = viewportRef.value
    if (!viewport) {
      return
    }

    viewport.scrollLeft = Math.max(0, (viewport.scrollWidth - viewport.clientWidth) / 2)
    viewport.scrollTop = 0
  })
}

async function mountViewer() {
  const currentSerial = ++loadSerial
  const host = containerRef.value
  const sourceUrl = normalizedUrl.value

  if (!host || !sourceUrl) {
    isLoading.value = false
    return
  }

  isLoading.value = true
  loadError.value = ''
  zoomScale.value = 100
  viewer.value = null
  host.innerHTML = ''

  try {
    const response = await fetch(sourceUrl)
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    const file = await response.arrayBuffer()
    if (currentSerial !== loadSerial || !containerRef.value) {
      return
    }

    host.innerHTML = ''
    const nextViewer = new XMindEmbedViewer({
      el: host,
      styles: {
        width: '100%',
        height: '100%',
        border: '0',
        background: '#ffffff',
      },
      region: 'global',
    })

    viewer.value = nextViewer
    nextViewer.addEventListener('map-ready', () => {
      nextViewer.setFitMap()
      zoomScale.value = nextViewer.zoom ?? 100
      centerViewport()
    })

    nextViewer.addEventListener('zoom-change', (payload: { zoomScale?: number }) => {
      if (typeof payload?.zoomScale === 'number') {
        zoomScale.value = payload.zoomScale
      }
    })

    nextViewer.load(file)
  } catch (error) {
    if (currentSerial !== loadSerial) {
      return
    }

    loadError.value = 'XMind 文件加载失败，请确认文件已正确上传。'
    console.error(error)
  } finally {
    if (currentSerial === loadSerial) {
      isLoading.value = false
    }
  }
}

function setZoom(scale: number) {
  if (!viewer.value) {
    return
  }

  viewer.value.setZoomScale(scale)
  zoomScale.value = scale
}

function zoomIn() {
  setZoom(Math.min(500, zoomScale.value + 10))
}

function zoomOut() {
  setZoom(Math.max(50, zoomScale.value - 10))
}

function fitMap() {
  viewer.value?.setFitMap()
  centerViewport()
}

function startPan(event: PointerEvent) {
  if (!isPanMode.value || !viewportRef.value) {
    return
  }

  isPanning.value = true
  panStart.value = {
    x: event.clientX,
    y: event.clientY,
    left: viewportRef.value.scrollLeft,
    top: viewportRef.value.scrollTop,
  }
  ;(event.currentTarget as HTMLElement).setPointerCapture(event.pointerId)
}

function movePan(event: PointerEvent) {
  if (!isPanning.value || !viewportRef.value) {
    return
  }

  const deltaX = event.clientX - panStart.value.x
  const deltaY = event.clientY - panStart.value.y
  viewportRef.value.scrollLeft = panStart.value.left - deltaX
  viewportRef.value.scrollTop = panStart.value.top - deltaY
}

function stopPan(event: PointerEvent) {
  if (!isPanning.value) {
    return
  }

  isPanning.value = false
  const target = event.currentTarget as HTMLElement
  if (target.hasPointerCapture(event.pointerId)) {
    target.releasePointerCapture(event.pointerId)
  }
}

function handlePanWheel(event: WheelEvent) {
  if (!isPanMode.value || !viewportRef.value) {
    return
  }

  viewportRef.value.scrollLeft += event.shiftKey ? event.deltaY : event.deltaX
  viewportRef.value.scrollTop += event.deltaY
}

watch(
  () => normalizedUrl.value,
  async () => {
    await nextTick()
    await mountViewer()
  },
  { immediate: true },
)

onBeforeUnmount(() => {
  loadSerial += 1
  if (containerRef.value) {
    containerRef.value.innerHTML = ''
  }
  viewer.value = null
})
</script>

<template>
  <div class="xmind-embed">
    <div class="toolbar">
      <div class="toolbar-copy">
        <strong>原始 XMind 导图</strong>
        <!-- <span>拖动模式可按住鼠标移动查看；交互模式保留 XMind 自带演示和节点操作。</span> -->
      </div>

      <div class="toolbar-actions">
        <!-- <button type="button" class="tool-btn primary" @click="togglePanMode">
          {{ isPanMode ? '切到交互模式' : '切到拖动模式' }}
        </button> -->
        <button type="button" class="tool-btn" @click="zoomOut">缩小</button>
        <span class="zoom-text">{{ zoomScale }}%</span>
        <button type="button" class="tool-btn" @click="zoomIn">放大</button>
        <button type="button" class="tool-btn" @click="fitMap">适应画布</button>
      </div>
    </div>

    <div v-if="loadError" class="status error">{{ loadError }}</div>
    <div v-else-if="isLoading" class="status">正在加载 XMind 导图...</div>

    <div
      class="viewer-shell"
      :class="{ hidden: isLoading || !!loadError, 'is-panning': isPanning }"
    >
      <div ref="viewportRef" class="viewer-viewport">
        <div ref="containerRef" class="viewer-host" :style="hostStyle"></div>
      </div>
      <div
        v-if="isPanMode"
        class="pan-layer"
        title="按住鼠标拖动画布；滚轮上下移动；如需使用 XMind 自带演示，请切到交互模式"
        @pointerdown="startPan"
        @pointermove="movePan"
        @pointerup="stopPan"
        @pointercancel="stopPan"
        @pointerleave="stopPan"
        @wheel.prevent="handlePanWheel"
      ></div>
    </div>
  </div>
</template>

<style scoped>
.xmind-embed {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 14px 18px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(255, 255, 255, 0.04);
}

.toolbar-copy {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.toolbar-copy strong {
  color: rgba(255, 255, 255, 0.92);
  font-size: 0.95rem;
}

.toolbar-copy span {
  color: rgba(255, 255, 255, 0.58);
  font-size: 0.85rem;
}

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.tool-btn {
  padding: 8px 14px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.9);
  cursor: pointer;
}

.tool-btn:hover {
  border-color: rgba(0, 191, 255, 0.4);
  color: #00ffff;
}

.tool-btn.primary {
  border-color: rgba(0, 191, 255, 0.28);
  background: rgba(0, 191, 255, 0.12);
  color: #00ffff;
}

.zoom-text {
  min-width: 58px;
  text-align: center;
  color: rgba(255, 255, 255, 0.68);
}

.status {
  padding: 18px 20px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(0, 191, 255, 0.12);
  color: rgba(255, 255, 255, 0.82);
}

.status.error {
  border-color: rgba(255, 59, 48, 0.24);
  color: #ff918b;
}

.viewer-shell {
  position: relative;
  height: 780px;
  border-radius: 18px;
  overflow: hidden;
  background: #ffffff;
}

.viewer-shell.hidden {
  display: none;
}

.viewer-shell.is-panning,
.viewer-shell.is-panning .pan-layer {
  cursor: grabbing;
}

.viewer-viewport {
  width: 100%;
  height: 100%;
  overflow: auto;
  scrollbar-color: rgba(0, 191, 255, 0.55) rgba(15, 23, 42, 0.08);
  scrollbar-width: thin;
}

.viewer-host {
  min-width: 100%;
  min-height: 100%;
  background: #ffffff;
}

.pan-layer {
  position: absolute;
  inset: 0;
  z-index: 2;
  cursor: grab;
  touch-action: none;
}

@media (max-width: 900px) {
  .toolbar {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
