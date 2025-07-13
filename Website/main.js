// Main JavaScript file for Krishi Mitra application
// Handles animations, UI interactions, and data updates

import { sensorManager } from './firebase.js';

// Application state
let isMenuOpen = false;
let animationInitialized = false;

// DOM elements
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');
const navLinks = document.querySelectorAll('.nav-link');

// Three.js variables for background animation
let scene, camera, renderer, particles;

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Krishi Mitra application starting...');
    
    initializeNavigation();
    initializeThreeJS();
    initializeAnimations();
    initializeSensorData();
    initializeScrollEffects();
    
    console.log('Application initialized successfully');
});

// Navigation functionality
function initializeNavigation() {
    // Mobile menu toggle
    if (hamburger) {
        hamburger.addEventListener('click', toggleMobileMenu);
    }

    // Close mobile menu when clicking on nav links
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (isMenuOpen) {
                toggleMobileMenu();
            }
        });
    });

    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Toggle mobile menu
function toggleMobileMenu() {
    isMenuOpen = !isMenuOpen;
    navMenu.classList.toggle('active');
    
    // Animate hamburger menu
    hamburger.classList.toggle('active');
    
    // Animate menu items
    if (isMenuOpen) {
        anime({
            targets: '.nav-menu .nav-item',
            translateY: [20, 0],
            opacity: [0, 1],
            delay: anime.stagger(100),
            duration: 300,
            easing: 'easeOutQuart'
        });
    }
}

// Initialize Three.js background animation
function initializeThreeJS() {
    const heroSection = document.querySelector('.hero-bg-animation');
    if (!heroSection) return;

    // Create scene
    scene = new THREE.Scene();
    
    // Create camera
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 5;
    
    // Create renderer
    renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(0x000000, 0);
    heroSection.appendChild(renderer.domElement);
    
    // Create particles system
    createParticleSystem();
    
    // Start animation loop
    animate();
    
    // Handle window resize
    window.addEventListener('resize', onWindowResize);
}

// Create floating particle system representing agriculture elements
function createParticleSystem() {
    const particleCount = 100;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);
    
    // Agricultural color palette
    const agriColors = [
        new THREE.Color(0x4caf50), // Green
        new THREE.Color(0x8bc34a), // Light Green
        new THREE.Color(0xffc107), // Yellow
        new THREE.Color(0xff9800), // Orange
        new THREE.Color(0x81c784)  // Medium Green
    ];
    
    for (let i = 0; i < particleCount; i++) {
        const i3 = i * 3;
        
        // Random positions
        positions[i3] = (Math.random() - 0.5) * 20;
        positions[i3 + 1] = (Math.random() - 0.5) * 20;
        positions[i3 + 2] = (Math.random() - 0.5) * 10;
        
        // Random colors from agricultural palette
        const color = agriColors[Math.floor(Math.random() * agriColors.length)];
        colors[i3] = color.r;
        colors[i3 + 1] = color.g;
        colors[i3 + 2] = color.b;
    }
    
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    
    // Create material
    const material = new THREE.PointsMaterial({
        size: 0.1,
        vertexColors: true,
        transparent: true,
        opacity: 0.8
    });
    
    // Create particles mesh
    particles = new THREE.Points(geometry, material);
    scene.add(particles);
}

// Animation loop for Three.js
function animate() {
    requestAnimationFrame(animate);
    
    if (particles) {
        // Rotate particles slowly
        particles.rotation.x += 0.001;
        particles.rotation.y += 0.002;
        
        // Move particles up and down
        const positions = particles.geometry.attributes.position.array;
        for (let i = 1; i < positions.length; i += 3) {
            positions[i] += Math.sin(Date.now() * 0.001 + i) * 0.001;
        }
        particles.geometry.attributes.position.needsUpdate = true;
    }
    
    renderer.render(scene, camera);
}

// Handle window resize for Three.js
function onWindowResize() {
    if (camera && renderer) {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }
}

// Initialize page animations with Anime.js
function initializeAnimations() {
    // Header animation on page load
    anime({
        targets: '.navbar',
        translateY: [-100, 0],
        opacity: [0, 1],
        duration: 800,
        easing: 'easeOutQuart',
        delay: 300
    });
    
    // Hero content animation
    anime({
        targets: '.hero-title',
        translateY: [50, 0],
        opacity: [0, 1],
        duration: 1000,
        easing: 'easeOutQuart',
        delay: 600
    });
    
    anime({
        targets: '.hero-description',
        translateY: [30, 0],
        opacity: [0, 1],
        duration: 800,
        easing: 'easeOutQuart',
        delay: 800
    });
    
    anime({
        targets: '.hero-buttons .btn',
        translateY: [30, 0],
        opacity: [0, 1],
        duration: 600,
        easing: 'easeOutQuart',
        delay: anime.stagger(200, {start: 1000})
    });
    
    animationInitialized = true;
}

// Initialize scroll-triggered animations
function initializeScrollEffects() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateElement(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    document.querySelectorAll('.feature-card, .data-card, .section-header').forEach(el => {
        observer.observe(el);
    });
}

// Animate individual elements when they come into view
function animateElement(element) {
    if (element.classList.contains('feature-card')) {
        anime({
            targets: element,
            translateY: [50, 0],
            opacity: [0, 1],
            duration: 600,
            easing: 'easeOutQuart'
        });
    } else if (element.classList.contains('data-card')) {
        anime({
            targets: element,
            scale: [0.8, 1],
            opacity: [0, 1],
            duration: 500,
            easing: 'easeOutBack'
        });
    } else if (element.classList.contains('section-header')) {
        anime({
            targets: element.querySelector('.section-title'),
            translateY: [30, 0],
            opacity: [0, 1],
            duration: 600,
            easing: 'easeOutQuart'
        });
        
        anime({
            targets: element.querySelector('.section-subtitle'),
            translateY: [20, 0],
            opacity: [0, 1],
            duration: 500,
            easing: 'easeOutQuart',
            delay: 200
        });
    }
}

// Initialize sensor data management
function initializeSensorData() {
    // Set up data update callback
    sensorManager.setDataUpdateCallback(updateSensorDisplay);
    
    // Start listening for data updates
    sensorManager.startListening();
    
    console.log('Sensor data monitoring started');
}

// Update sensor data display on the page
function updateSensorDisplay(data) {
    // Update temperature
    const tempElement = document.getElementById('temperature');
    const tempStatus = document.getElementById('tempStatus');
    if (tempElement) {
        tempElement.textContent = data.temperature;
        updateStatus(tempStatus, parseFloat(data.temperature), 15, 35, '°C');
    }
    
    // Update humidity
    const humidityElement = document.getElementById('humidity');
    const humidityStatus = document.getElementById('humidityStatus');
    if (humidityElement) {
        humidityElement.textContent = data.humidity;
        updateStatus(humidityStatus, parseFloat(data.humidity), 40, 70, '%');
    }
    
    // Update soil moisture
    const soilElement = document.getElementById('soilMoisture');
    const soilStatus = document.getElementById('soilStatus');
    if (soilElement) {
        soilElement.textContent = data.soilMoisture;
        updateStatus(soilStatus, parseFloat(data.soilMoisture), 30, 80, '%');
    }
    
    // Update rainfall
    const rainfallElement = document.getElementById('rainfall');
    const rainStatus = document.getElementById('rainStatus');
    if (rainfallElement) {
        rainfallElement.textContent = data.rainfall;
        updateRainStatus(rainStatus, parseFloat(data.rainfall));
    }
    
    // Update last updated time
    const lastUpdatedElement = document.getElementById('lastUpdated');
    if (lastUpdatedElement) {
        const date = new Date(data.lastUpdated);
        lastUpdatedElement.textContent = date.toLocaleTimeString();
    }
    
    // Animate value updates
    animateDataUpdate();
}

// Update status indicators with appropriate styling
function updateStatus(statusElement, value, minGood, maxGood, unit) {
    if (!statusElement) return;
    
    let status = 'Normal';
    let className = '';
    
    if (value < minGood) {
        status = 'Low';
        className = 'warning';
    } else if (value > maxGood) {
        status = 'High';
        className = 'danger';
    } else {
        status = 'Optimal';
        className = '';
    }
    
    statusElement.textContent = status;
    statusElement.className = 'data-status ' + className;
}

// Update rain status specifically
function updateRainStatus(statusElement, rainfall) {
    if (!statusElement) return;
    
    let status = 'No Rain';
    let className = '';
    
    if (rainfall > 0 && rainfall <= 2) {
        status = 'Light Rain';
        className = '';
    } else if (rainfall > 2 && rainfall <= 7) {
        status = 'Moderate Rain';
        className = 'warning';
    } else if (rainfall > 7) {
        status = 'Heavy Rain';
        className = 'danger';
    }
    
    statusElement.textContent = status;
    statusElement.className = 'data-status ' + className;
}

// Animate data updates
function animateDataUpdate() {
    anime({
        targets: '.data-value',
        scale: [1.1, 1],
        duration: 300,
        easing: 'easeOutQuart'
    });
}

// Utility function to scroll to a specific section
window.scrollToSection = function(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
};

// Handle page visibility changes to optimize performance
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // Pause animations when page is not visible
        if (renderer) {
            renderer.setAnimationLoop(null);
        }
    } else {
        // Resume animations when page becomes visible
        if (renderer) {
            renderer.setAnimationLoop(animate);
        }
    }
});

// Clean up on page unload
window.addEventListener('beforeunload', function() {
    if (sensorManager) {
        sensorManager.stopListening();
    }
    
    if (renderer) {
        renderer.dispose();
    }
});

// Create local reference for export
const exportedScrollToSection = window.scrollToSection;

// Export functions for external use
export { 
    toggleMobileMenu, 
    animateElement, 
    updateSensorDisplay,
    exportedScrollToSection as scrollToSection
};