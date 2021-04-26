<template>
  <div
    ref="container"
    class="split-pane"
    :class="{ dragging: isDragging }"
    @mousemove="onDragging"
    @mouseup="stopDragging"
    @mouseleave="stopDragging"
  >
    <div class="left" :style="{ width: getWidth() + '%' }">
      <slot name="left" />
      <div class="split-line" @mousedown.prevent="startDragging" />
    </div>
    <div class="right" :style="{ width: 100 - getWidth() + '%' }">
      <slot name="right" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      width: 50,
      isDragging: false
    }
  },
  methods: {
    getWidth() {
      return this.width < 20 ? 20 : this.width > 80 ? 80 : this.width
    },
    onDragging(e) {
      if (this.isDragging) {
        const draggingPosition = e.pageX
        const totalSize = this.$refs.container.offsetWidth
        this.width = (draggingPosition / totalSize) * 100
      }
    },
    startDragging() {
      this.isDragging = true
    },
    stopDragging() {
      this.isDragging = false
    }
  }
}
</script>

<style scoped>
.split-pane {
  display: flex;
  height: 100%;
}
.split-pane.dragging {
  cursor: ew-resize;
}
.dragging .left,
.dragging .right {
  pointer-events: none;
}
.left,
.right {
  position: relative;
  height: 100%;
}
.left {
  border-right: 1px solid var(--c-white-dark);
}
.split-line {
  position: absolute;
  z-index: 99;
  top: 0;
  bottom: 0;
  right: -5px;
  width: 10px;
  cursor: ew-resize;
}
</style>
