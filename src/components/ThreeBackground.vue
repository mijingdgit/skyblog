<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import type * as ThreeNamespace from 'three'

const containerRef = ref<HTMLDivElement>()
let THREE: typeof ThreeNamespace | null = null
let scene: ThreeNamespace.Scene
let camera: ThreeNamespace.PerspectiveCamera
let renderer: ThreeNamespace.WebGLRenderer
let particles: ThreeNamespace.Points
let geometries: ThreeNamespace.Mesh[] = []
let animationId: number
let deferredStartId: number | undefined
let disposed = false

const mouse = { x: 0, y: 0 }

const getThree = () => {
  if (!THREE) {
    throw new Error('Three.js has not been loaded yet.')
  }

  return THREE
}

const getParticleCount = () => {
  const isSmallScreen = window.innerWidth < 768
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches

  if (prefersReducedMotion) {
    return 320
  }

  return isSmallScreen ? 800 : 1400
}

const initThree = async () => {
  if (!containerRef.value) return

  THREE = await import('three')

  if (disposed || !containerRef.value) {
    return
  }

  const three = getThree()

  // Scene
  scene = new three.Scene()
  scene.fog = new three.FogExp2(0x0a0a1a, 0.002)

  // Camera
  camera = new three.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  )
  camera.position.z = 50

  // Renderer
  renderer = new three.WebGLRenderer({ antialias: false, alpha: true, powerPreference: 'low-power' })
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5))
  renderer.setClearColor(0x0a0a1a, 1)
  containerRef.value.appendChild(renderer.domElement)

  // Particles
  createParticles()

  // Geometries
  createGeometries()

  // Lights
  const ambientLight = new three.AmbientLight(0x00bfff, 0.5)
  scene.add(ambientLight)

  const pointLight1 = new three.PointLight(0x00ffff, 2, 100)
  pointLight1.position.set(20, 20, 20)
  scene.add(pointLight1)

  const pointLight2 = new three.PointLight(0x00bfff, 2, 100)
  pointLight2.position.set(-20, -20, 20)
  scene.add(pointLight2)
}

const createParticles = () => {
  const three = getThree()
  const geometry = new three.BufferGeometry()
  const count = getParticleCount()
  const positions = new Float32Array(count * 3)
  const colors = new Float32Array(count * 3)
  const sizes = new Float32Array(count)

  const colorPalette = [
    new three.Color(0x00bfff),
    new three.Color(0x00ffff),
    new three.Color(0x1e90ff),
    new three.Color(0x14b8a6),
  ]

  for (let i = 0; i < count; i++) {
    const i3 = i * 3
    positions[i3] = (Math.random() - 0.5) * 200
    positions[i3 + 1] = (Math.random() - 0.5) * 200
    positions[i3 + 2] = (Math.random() - 0.5) * 200

    const color = colorPalette[Math.floor(Math.random() * colorPalette.length)]
    colors[i3] = color.r
    colors[i3 + 1] = color.g
    colors[i3 + 2] = color.b

    sizes[i] = Math.random() * 2
  }

  geometry.setAttribute('position', new three.BufferAttribute(positions, 3))
  geometry.setAttribute('color', new three.BufferAttribute(colors, 3))
  geometry.setAttribute('size', new three.BufferAttribute(sizes, 1))

  const material = new three.PointsMaterial({
    size: 0.5,
    vertexColors: true,
    transparent: true,
    opacity: 0.8,
    blending: three.AdditiveBlending,
  })

  particles = new three.Points(geometry, material)
  scene.add(particles)
}

const createGeometries = () => {
  const three = getThree()

  // Cube
  const cubeGeo = new three.BoxGeometry(3, 3, 3)
  const cubeMat = new three.MeshStandardMaterial({
    color: 0x00bfff,
    emissive: 0x00bfff,
    emissiveIntensity: 0.3,
    wireframe: true,
  })
  const cube = new three.Mesh(cubeGeo, cubeMat)
  cube.position.set(-15, 10, -20)
  scene.add(cube)
  geometries.push(cube)

  // Octahedron
  const octaGeo = new three.OctahedronGeometry(2.5)
  const octaMat = new three.MeshStandardMaterial({
    color: 0x00ffff,
    emissive: 0x00ffff,
    emissiveIntensity: 0.3,
    wireframe: true,
  })
  const octa = new three.Mesh(octaGeo, octaMat)
  octa.position.set(20, -5, -30)
  scene.add(octa)
  geometries.push(octa)

  // Icosahedron
  const icoGeo = new three.IcosahedronGeometry(2)
  const icoMat = new three.MeshStandardMaterial({
    color: 0x1e90ff,
    emissive: 0x1e90ff,
    emissiveIntensity: 0.3,
    wireframe: true,
  })
  const ico = new three.Mesh(icoGeo, icoMat)
  ico.position.set(0, -15, -25)
  scene.add(ico)
  geometries.push(ico)

  // Torus
  const torusGeo = new three.TorusGeometry(2, 0.5, 16, 72)
  const torusMat = new three.MeshStandardMaterial({
    color: 0x14b8a6,
    emissive: 0x14b8a6,
    emissiveIntensity: 0.3,
    wireframe: true,
  })
  const torus = new three.Mesh(torusGeo, torusMat)
  torus.position.set(15, 15, -35)
  scene.add(torus)
  geometries.push(torus)
}

const animate = () => {
  if (disposed || !renderer) {
    return
  }

  animationId = requestAnimationFrame(animate)

  // Rotate particles slightly
  if (particles) {
    particles.rotation.y += 0.0005
    particles.rotation.x += 0.0002
  }

  // Rotate geometries
  geometries.forEach((geo, index) => {
    geo.rotation.x += 0.005 * (index % 2 === 0 ? 1 : -1)
    geo.rotation.y += 0.007 * (index % 2 === 0 ? 1 : -1)
  })

  // Mouse interaction
  if (particles) {
    const positions = particles.geometry.attributes.position.array as Float32Array
    for (let i = 0; i < positions.length; i += 3) {
      positions[i] += mouse.x * 0.01
      positions[i + 1] += mouse.y * 0.01
    }
    particles.geometry.attributes.position.needsUpdate = true
  }

  renderer.render(scene, camera)
}

const handleMouseMove = (e: MouseEvent) => {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1
}

const handleResize = () => {
  if (!camera || !renderer) return
  camera.aspect = window.innerWidth / window.innerHeight
  camera.updateProjectionMatrix()
  renderer.setSize(window.innerWidth, window.innerHeight)
}

const startThree = async () => {
  await initThree()

  if (!disposed) {
    animate()
  }

  window.addEventListener('mousemove', handleMouseMove)
  window.addEventListener('resize', handleResize)
}

onMounted(() => {
  disposed = false
  const start = () => {
    void startThree()
  }

  if ('requestIdleCallback' in window) {
    deferredStartId = window.requestIdleCallback(start, { timeout: 1200 })
  } else {
    deferredStartId = globalThis.setTimeout(start, 600)
  }
})

onUnmounted(() => {
  disposed = true
  if (deferredStartId !== undefined) {
    if ('cancelIdleCallback' in window) {
      window.cancelIdleCallback(deferredStartId)
    }
    window.clearTimeout(deferredStartId)
  }
  cancelAnimationFrame(animationId)
  window.removeEventListener('mousemove', handleMouseMove)
  window.removeEventListener('resize', handleResize)
  geometries.forEach((mesh) => {
    mesh.geometry.dispose()
    if (Array.isArray(mesh.material)) {
      mesh.material.forEach((material) => material.dispose())
    } else {
      mesh.material.dispose()
    }
  })
  particles?.geometry.dispose()
  const particleMaterial = particles?.material
  if (Array.isArray(particleMaterial)) {
    particleMaterial.forEach((material) => material.dispose())
  } else {
    particleMaterial?.dispose()
  }
  renderer?.dispose()
  renderer?.domElement.remove()
  geometries = []
})
</script>

<template>
  <div ref="containerRef" class="three-container"></div>
</template>

<style scoped>
.three-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
}
</style>
