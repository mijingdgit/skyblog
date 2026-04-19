<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'

const containerRef = ref<HTMLDivElement>()
let scene: THREE.Scene
let camera: THREE.PerspectiveCamera
let renderer: THREE.WebGLRenderer
let particles: THREE.Points
let geometries: THREE.Mesh[] = []
let animationId: number

const mouse = { x: 0, y: 0 }

const initThree = () => {
  if (!containerRef.value) return

  // Scene
  scene = new THREE.Scene()
  scene.fog = new THREE.FogExp2(0x0a0a1a, 0.002)

  // Camera
  camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  )
  camera.position.z = 50

  // Renderer
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.setClearColor(0x0a0a1a, 1)
  containerRef.value.appendChild(renderer.domElement)

  // Particles
  createParticles()

  // Geometries
  createGeometries()

  // Lights
  const ambientLight = new THREE.AmbientLight(0x00bfff, 0.5)
  scene.add(ambientLight)

  const pointLight1 = new THREE.PointLight(0x00ffff, 2, 100)
  pointLight1.position.set(20, 20, 20)
  scene.add(pointLight1)

  const pointLight2 = new THREE.PointLight(0x00bfff, 2, 100)
  pointLight2.position.set(-20, -20, 20)
  scene.add(pointLight2)
}

const createParticles = () => {
  const geometry = new THREE.BufferGeometry()
  const count = 2000
  const positions = new Float32Array(count * 3)
  const colors = new Float32Array(count * 3)
  const sizes = new Float32Array(count)

  const colorPalette = [
    new THREE.Color(0x00bfff),
    new THREE.Color(0x00ffff),
    new THREE.Color(0x1e90ff),
    new THREE.Color(0x14b8a6),
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

  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))
  geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1))

  const material = new THREE.PointsMaterial({
    size: 0.5,
    vertexColors: true,
    transparent: true,
    opacity: 0.8,
    blending: THREE.AdditiveBlending,
  })

  particles = new THREE.Points(geometry, material)
  scene.add(particles)
}

const createGeometries = () => {
  // Cube
  const cubeGeo = new THREE.BoxGeometry(3, 3, 3)
  const cubeMat = new THREE.MeshStandardMaterial({
    color: 0x00bfff,
    emissive: 0x00bfff,
    emissiveIntensity: 0.3,
    wireframe: true,
  })
  const cube = new THREE.Mesh(cubeGeo, cubeMat)
  cube.position.set(-15, 10, -20)
  scene.add(cube)
  geometries.push(cube)

  // Octahedron
  const octaGeo = new THREE.OctahedronGeometry(2.5)
  const octaMat = new THREE.MeshStandardMaterial({
    color: 0x00ffff,
    emissive: 0x00ffff,
    emissiveIntensity: 0.3,
    wireframe: true,
  })
  const octa = new THREE.Mesh(octaGeo, octaMat)
  octa.position.set(20, -5, -30)
  scene.add(octa)
  geometries.push(octa)

  // Icosahedron
  const icoGeo = new THREE.IcosahedronGeometry(2)
  const icoMat = new THREE.MeshStandardMaterial({
    color: 0x1e90ff,
    emissive: 0x1e90ff,
    emissiveIntensity: 0.3,
    wireframe: true,
  })
  const ico = new THREE.Mesh(icoGeo, icoMat)
  ico.position.set(0, -15, -25)
  scene.add(ico)
  geometries.push(ico)

  // Torus
  const torusGeo = new THREE.TorusGeometry(2, 0.5, 16, 100)
  const torusMat = new THREE.MeshStandardMaterial({
    color: 0x14b8a6,
    emissive: 0x14b8a6,
    emissiveIntensity: 0.3,
    wireframe: true,
  })
  const torus = new THREE.Mesh(torusGeo, torusMat)
  torus.position.set(15, 15, -35)
  scene.add(torus)
  geometries.push(torus)
}

const animate = () => {
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

onMounted(() => {
  initThree()
  animate()
  window.addEventListener('mousemove', handleMouseMove)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  cancelAnimationFrame(animationId)
  window.removeEventListener('mousemove', handleMouseMove)
  window.removeEventListener('resize', handleResize)
  renderer?.dispose()
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